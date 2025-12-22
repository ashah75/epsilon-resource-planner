"""Object-oriented backend API for epsilon-resource-planner.

This module exposes a Flask application that manages people, clients,
projects, and assignments backed by SQLite. The design follows an
object-oriented structure to align with SOLID principles and keeps
security-focused practices such as input validation and parameterized
queries. A helper is provided to connect to any relational database
supported by SQLAlchemy-compatible URLs.
"""

from __future__ import annotations

import logging
import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Mapping, Protocol, Sequence

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


def _resolve_sqlite_path(db_url: str) -> str:
    """Return a filesystem path for a SQLite URL or raw path."""

    if db_url.startswith("sqlite:///"):
        return db_url.replace("sqlite:///", "", 1)
    return db_url


@dataclass(frozen=True)
class DatabaseConfig:
    """Configuration holder for database connectivity."""

    sqlite_url: str = os.environ.get("DATABASE_URL", "sqlite:///resource_planner.db")

    @property
    def sqlite_path(self) -> str:
        return _resolve_sqlite_path(self.sqlite_url)


# ---------------------------------------------------------------------------
# Database access
# ---------------------------------------------------------------------------


class ConnectionProvider(Protocol):
    """Protocol for obtaining database connections."""

    def get_connection(self) -> sqlite3.Connection:
        ...


class SQLiteConnectionProvider:
    """Create SQLite connections with secure defaults."""

    def __init__(self, config: DatabaseConfig) -> None:
        self._config = config

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self._config.sqlite_path, detect_types=sqlite3.PARSE_DECLTYPES
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn


def create_db_connection(connection_url: str):
    """Create a connection to a relational database using SQLAlchemy URLs."""

    from sqlalchemy import create_engine

    engine = create_engine(connection_url, pool_pre_ping=True, future=True)
    return engine.connect()


# ---------------------------------------------------------------------------
# Data repositories
# ---------------------------------------------------------------------------


class BaseRepository:
    """Base repository that provides context-managed execution helpers."""

    def __init__(self, connection_provider: ConnectionProvider) -> None:
        self._connection_provider = connection_provider

    def _execute(self, query: str, parameters: Sequence[Any] = ()):
        with self._connection_provider.get_connection() as conn:
            return conn.execute(query, parameters)

    def _fetchall(self, query: str, parameters: Sequence[Any] = ()) -> List[Dict[str, Any]]:
        rows = self._execute(query, parameters).fetchall()
        return [dict(row) for row in rows]

    def _fetchone(self, query: str, parameters: Sequence[Any] = ()) -> Dict[str, Any] | None:
        row = self._execute(query, parameters).fetchone()
        return dict(row) if row else None


class PeopleRepository(BaseRepository):
    def list(self) -> List[Dict[str, Any]]:
        return self._fetchall("SELECT * FROM people")

    def create(self, name: str, role: str) -> int:
        cursor = self._execute("INSERT INTO people (name, role) VALUES (?, ?)", (name, role))
        return cursor.lastrowid

    def delete(self, person_id: int) -> None:
        with self._connection_provider.get_connection() as conn:
            conn.execute("DELETE FROM assignments WHERE person_id = ?", (person_id,))
            conn.execute("DELETE FROM people WHERE id = ?", (person_id,))

    def update(self, person_id: int, name: str, role: str) -> None:
        self._execute("UPDATE people SET name = ?, role = ? WHERE id = ?", (name, role, person_id))

    def get_id_by_name(self, name: str) -> int | None:
        row = self._fetchone("SELECT id FROM people WHERE LOWER(name) = LOWER(?)", (name,))
        return row["id"] if row else None


class ClientsRepository(BaseRepository):
    def list(self) -> List[Dict[str, Any]]:
        return self._fetchall("SELECT * FROM clients")

    def create(self, name: str) -> int:
        cursor = self._execute("INSERT INTO clients (name) VALUES (?)", (name,))
        return cursor.lastrowid

    def delete(self, client_id: int) -> None:
        with self._connection_provider.get_connection() as conn:
            projects = conn.execute("SELECT id FROM projects WHERE client_id = ?", (client_id,)).fetchall()
            project_ids = [project["id"] for project in projects]
            for project_id in project_ids:
                conn.execute("DELETE FROM assignments WHERE project_id = ?", (project_id,))
            conn.execute("DELETE FROM projects WHERE client_id = ?", (client_id,))
            conn.execute("DELETE FROM clients WHERE id = ?", (client_id,))

    def update(self, client_id: int, name: str) -> None:
        self._execute("UPDATE clients SET name = ? WHERE id = ?", (name, client_id))

    def get_id_by_name(self, name: str) -> int | None:
        row = self._fetchone("SELECT id FROM clients WHERE LOWER(name) = LOWER(?)", (name,))
        return row["id"] if row else None


class ProjectsRepository(BaseRepository):
    def list(self) -> List[Dict[str, Any]]:
        return self._fetchall("SELECT * FROM projects")

    def create(self, name: str, client_id: int) -> int:
        cursor = self._execute(
            "INSERT INTO projects (name, client_id) VALUES (?, ?)", (name, client_id)
        )
        return cursor.lastrowid

    def delete(self, project_id: int) -> None:
        with self._connection_provider.get_connection() as conn:
            conn.execute("DELETE FROM assignments WHERE project_id = ?", (project_id,))
            conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))

    def update(self, project_id: int, name: str, client_id: int) -> None:
        self._execute(
            "UPDATE projects SET name = ?, client_id = ? WHERE id = ?",
            (name, client_id, project_id),
        )

    def get_id_by_name(self, name: str) -> int | None:
        row = self._fetchone("SELECT id FROM projects WHERE LOWER(name) = LOWER(?)", (name,))
        return row["id"] if row else None

    def get_id_by_name_and_client(self, name: str, client_id: int) -> int | None:
        row = self._fetchone(
            "SELECT id FROM projects WHERE LOWER(name) = LOWER(?) AND client_id = ?",
            (name, client_id),
        )
        return row["id"] if row else None


class AssignmentsRepository(BaseRepository):
    def list(self) -> List[Dict[str, Any]]:
        return self._fetchall("SELECT * FROM assignments")

    def create(
        self,
        person_id: int,
        project_id: int,
        start_date: str,
        end_date: str,
        percentage: int,
    ) -> int:
        cursor = self._execute(
            """
            INSERT INTO assignments (person_id, project_id, start_date, end_date, percentage)
            VALUES (?, ?, ?, ?, ?)
            """,
            (person_id, project_id, start_date, end_date, percentage),
        )
        return cursor.lastrowid

    def find_existing(
        self, person_id: int, project_id: int, start_date: str, end_date: str
    ) -> int | None:
        row = self._fetchone(
            """
            SELECT id FROM assignments
            WHERE person_id = ? AND project_id = ? AND start_date = ? AND end_date = ?
            """,
            (person_id, project_id, start_date, end_date),
        )
        return row["id"] if row else None

    def delete(self, assignment_id: int) -> None:
        self._execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))

    def update(
        self,
        assignment_id: int,
        person_id: int,
        project_id: int,
        start_date: str,
        end_date: str,
        percentage: int,
    ) -> None:
        self._execute(
            """
            UPDATE assignments
            SET person_id = ?, project_id = ?, start_date = ?, end_date = ?, percentage = ?
            WHERE id = ?
            """,
            (person_id, project_id, start_date, end_date, percentage, assignment_id),
        )


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------


class ValidationService:
    """Handle input validation concerns."""

    @staticmethod
    def _camel_to_snake(value: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()

    @staticmethod
    def require_json(
        required_fields: Iterable[str], aliases: Mapping[str, Iterable[str]] | None = None
    ) -> Dict[str, Any]:
        if not request.is_json:
            abort(400, description="Request must be JSON")

        data = request.get_json() or {}
        normalized: Dict[str, Any] = dict(data)

        # Accept snake_case fallbacks for camelCase field names
        for field in required_fields:
            snake_fallback = ValidationService._camel_to_snake(field)
            if field not in normalized and snake_fallback in normalized:
                normalized[field] = normalized[snake_fallback]

        # Explicit alias mapping when provided
        if aliases:
            for canonical, alias_keys in aliases.items():
                if canonical in normalized:
                    continue
                for alias in alias_keys:
                    if alias in normalized:
                        normalized[canonical] = normalized[alias]
                        break

        missing = [field for field in required_fields if field not in normalized]
        if missing:
            abort(400, description=f"Missing required fields: {', '.join(missing)}")

        return normalized

    @staticmethod
    def convert_period_to_dates(period: int) -> Dict[str, str]:
        base_date = datetime(2026, 1, 1)
        period_start = base_date + timedelta(days=period * 14)
        period_end = period_start + timedelta(days=13)
        return {
            "start": period_start.strftime("%Y-%m-%d"),
            "end": period_end.strftime("%Y-%m-%d"),
        }


class BulkUploadService:
    def __init__(
        self,
        people_repo: PeopleRepository,
        clients_repo: ClientsRepository,
        projects_repo: ProjectsRepository,
        assignments_repo: AssignmentsRepository,
    ) -> None:
        self._people_repo = people_repo
        self._clients_repo = clients_repo
        self._projects_repo = projects_repo
        self._assignments_repo = assignments_repo

    def bulk_people(self, people_payload: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        added: List[Dict[str, Any]] = []
        for person in people_payload:
            new_id = self._people_repo.create(person["name"], person["role"])
            added.append({"id": new_id, "name": person["name"], "role": person["role"]})
        return added

    def bulk_clients(self, clients_payload: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        added: List[Dict[str, Any]] = []
        for client in clients_payload:
            new_id = self._clients_repo.create(client["name"])
            added.append({"id": new_id, "name": client["name"]})
        return added

    def bulk_projects(self, projects_payload: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        added: List[Dict[str, Any]] = []
        for project in projects_payload:
            client_id = project.get("clientId")
            if client_id is None:
                client_name = project.get("clientName") or project.get("client_name")
                if not client_name:
                    raise ValueError("Project requires clientId or clientName")
                client_id = self._clients_repo.get_id_by_name(client_name)
                if client_id is None:
                    raise ValueError(f"Client not found: {client_name}")

            new_id = self._projects_repo.create(project["name"], client_id)
            added.append({"id": new_id, "name": project["name"], "clientId": client_id})
        return added

    def bulk_assignments(self, assignments_payload: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        added: List[Dict[str, Any]] = []
        for assignment in assignments_payload:
            def _clean_name(value: Any) -> str | None:
                if value is None:
                    return None
                if isinstance(value, str):
                    trimmed = value.strip()
                    return trimmed if trimmed else None
                return str(value)

            start_date = assignment.get("startDate") or assignment.get("start_date")
            end_date = assignment.get("endDate") or assignment.get("end_date")
            if not start_date or not end_date:
                raise ValueError("Assignment requires startDate/start_date and endDate/end_date")

            person_id = assignment.get("personId") or assignment.get("person_id")
            if isinstance(person_id, str) and person_id.strip():
                try:
                    person_id = int(person_id)
                except ValueError:
                    raise ValueError("Assignment personId must be a number") from None
            if person_id is None:
                person_name = _clean_name(assignment.get("personName") or assignment.get("person_name"))
                if not person_name:
                    raise ValueError("Assignment requires personId or personName")
                person_id = self._people_repo.get_id_by_name(person_name)
                if person_id is None:
                    raise ValueError(f"Person not found: {person_name}")

            project_id = assignment.get("projectId") or assignment.get("project_id")
            if isinstance(project_id, str) and project_id.strip():
                try:
                    project_id = int(project_id)
                except ValueError:
                    raise ValueError("Assignment projectId must be a number") from None
            if project_id is None:
                project_name = _clean_name(assignment.get("projectName") or assignment.get("project_name"))
                client_name = _clean_name(assignment.get("clientName") or assignment.get("client_name"))
                if not project_name or not client_name:
                    raise ValueError("Assignment requires projectId or projectName with clientName")
                client_id = self._clients_repo.get_id_by_name(client_name)
                if client_id is None:
                    raise ValueError(f"Client not found: {client_name}")
                project_id = self._projects_repo.get_id_by_name_and_client(project_name, client_id)
                if project_id is None:
                    raise ValueError(f"Project not found: {project_name} (client: {client_name})")

            percentage = assignment.get("percentage", 100)
            if percentage in ("", None):
                percentage = 100
            try:
                percentage = int(percentage)
            except (TypeError, ValueError):
                raise ValueError("Assignment percentage must be a number") from None
            new_id = self._assignments_repo.create(
                person_id,
                project_id,
                start_date,
                end_date,
                percentage,
            )
            added.append(
                {
                    "id": new_id,
                    "personId": person_id,
                    "projectId": project_id,
                    "startDate": start_date,
                    "endDate": end_date,
                    "percentage": percentage,
                }
            )
        return added


class DatabaseInitializer:
    """Handle creation of database schema."""

    def __init__(self, connection_provider: ConnectionProvider) -> None:
        self._connection_provider = connection_provider

    def initialize(self) -> None:
        with self._connection_provider.get_connection() as conn:
            conn.executescript(
                """
                PRAGMA foreign_keys = ON;

                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    client_id INTEGER NOT NULL,
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                );

                CREATE TABLE IF NOT EXISTS assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER NOT NULL,
                    project_id INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    percentage INTEGER DEFAULT 100,
                    FOREIGN KEY (person_id) REFERENCES people(id),
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                );
                """
            )


# ---------------------------------------------------------------------------
# API Application
# ---------------------------------------------------------------------------


class ResourcePlannerAPI:
    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config
        self.app = Flask(__name__)
        CORS(self.app)

        self.connection_provider = SQLiteConnectionProvider(config)
        self.db_initializer = DatabaseInitializer(self.connection_provider)

        self.people_repo = PeopleRepository(self.connection_provider)
        self.clients_repo = ClientsRepository(self.connection_provider)
        self.projects_repo = ProjectsRepository(self.connection_provider)
        self.assignments_repo = AssignmentsRepository(self.connection_provider)
        self.bulk_service = BulkUploadService(
            self.people_repo, self.clients_repo, self.projects_repo, self.assignments_repo
        )

        self._register_routes()

    def _normalize_assignment_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not payload:
            abort(400, description="Assignment payload is required")

        def _clean_name(value: Any) -> str | None:
            if value is None:
                return None
            if isinstance(value, str):
                trimmed = value.strip()
                return trimmed if trimmed else None
            return str(value)

        person_id = payload.get("personId") or payload.get("person_id")
        if isinstance(person_id, str) and person_id.strip():
            try:
                person_id = int(person_id)
            except ValueError:
                abort(400, description="Assignment personId must be a number")
        if person_id is None:
            person_name = _clean_name(payload.get("personName") or payload.get("person_name"))
            if not person_name:
                abort(400, description="Assignment requires personId or personName")
            person_id = self.people_repo.get_id_by_name(person_name)
            if person_id is None:
                abort(400, description=f"Person not found: {person_name}")

        project_id = payload.get("projectId") or payload.get("project_id")
        if isinstance(project_id, str) and project_id.strip():
            try:
                project_id = int(project_id)
            except ValueError:
                abort(400, description="Assignment projectId must be a number")
        if project_id is None:
            project_name = _clean_name(payload.get("projectName") or payload.get("project_name"))
            client_name = _clean_name(payload.get("clientName") or payload.get("client_name"))
            if not project_name or not client_name:
                abort(400, description="Assignment requires projectId or projectName with clientName")
            client_id = self.clients_repo.get_id_by_name(client_name)
            if client_id is None:
                abort(400, description=f"Client not found: {client_name}")
            project_id = self.projects_repo.get_id_by_name_and_client(project_name, client_id)
            if project_id is None:
                abort(400, description=f"Project not found: {project_name} (client: {client_name})")

        start_date = payload.get("startDate") or payload.get("start_date")
        end_date = payload.get("endDate") or payload.get("end_date")
        if not start_date or not end_date:
            if "period" in payload:
                dates = ValidationService.convert_period_to_dates(int(payload["period"]))
                start_date = dates["start"]
                end_date = dates["end"]
            else:
                abort(400, description="Either startDate/endDate or period is required")

        percentage = payload.get("percentage", 100)
        if percentage in ("", None):
            percentage = 100
        try:
            percentage = int(percentage)
        except (TypeError, ValueError):
            abort(400, description="Assignment percentage must be a number")

        return {
            "personId": person_id,
            "projectId": project_id,
            "startDate": start_date,
            "endDate": end_date,
            "percentage": percentage,
        }

    # ---------------------------- Routes ---------------------------------
    def _register_routes(self) -> None:
        app = self.app

        @app.route("/api/people", methods=["GET"])
        def get_people():
            people = self.people_repo.list()
            return jsonify(people)

        @app.route("/api/people", methods=["POST"])
        def add_person():
            data = ValidationService.require_json({"name", "role"})
            person_id = self.people_repo.create(data["name"], data["role"])
            return jsonify({"id": person_id, "name": data["name"], "role": data["role"]}), 201

        @app.route("/api/people/<int:person_id>", methods=["DELETE"])
        def delete_person(person_id: int):
            self.people_repo.delete(person_id)
            return jsonify({"success": True}), 200

        @app.route("/api/people/<int:person_id>", methods=["PUT"])
        def update_person(person_id: int):
            data = ValidationService.require_json({"name", "role"})
            self.people_repo.update(person_id, data["name"], data["role"])
            return jsonify({"id": person_id, "name": data["name"], "role": data["role"]}), 200

        @app.route("/api/clients", methods=["GET"])
        def get_clients():
            clients = self.clients_repo.list()
            return jsonify(clients)

        @app.route("/api/clients", methods=["POST"])
        def add_client():
            data = ValidationService.require_json({"name"})
            client_id = self.clients_repo.create(data["name"])
            return jsonify({"id": client_id, "name": data["name"]}), 201

        @app.route("/api/clients/<int:client_id>", methods=["DELETE"])
        def delete_client(client_id: int):
            self.clients_repo.delete(client_id)
            return jsonify({"success": True}), 200

        @app.route("/api/clients/<int:client_id>", methods=["PUT"])
        def update_client(client_id: int):
            data = ValidationService.require_json({"name"})
            self.clients_repo.update(client_id, data["name"])
            return jsonify({"id": client_id, "name": data["name"]}), 200

        @app.route("/api/projects", methods=["GET"])
        def get_projects():
            projects = self.projects_repo.list()
            return jsonify(projects)

        @app.route("/api/projects", methods=["POST"])
        def add_project():
            data = ValidationService.require_json({"name", "clientId"})
            project_id = self.projects_repo.create(data["name"], data["clientId"])
            return jsonify({"id": project_id, "name": data["name"], "clientId": data["clientId"]}), 201

        @app.route("/api/projects/<int:project_id>", methods=["DELETE"])
        def delete_project(project_id: int):
            self.projects_repo.delete(project_id)
            return jsonify({"success": True}), 200

        @app.route("/api/projects/<int:project_id>", methods=["PUT"])
        def update_project(project_id: int):
            data = ValidationService.require_json({"name", "clientId"})
            self.projects_repo.update(project_id, data["name"], data["clientId"])
            return jsonify({"id": project_id, "name": data["name"], "clientId": data["clientId"]}), 200

        @app.route("/api/assignments", methods=["GET"])
        def get_assignments():
            assignments = self.assignments_repo.list()
            return jsonify(assignments)

        @app.route("/api/assignments", methods=["POST"])
        def add_assignment():
            if not request.is_json:
                abort(400, description="Request must be JSON")
            data = request.get_json() or {}
            normalized = self._normalize_assignment_payload(data)
            assignment_id = self.assignments_repo.create(
                normalized["personId"],
                normalized["projectId"],
                normalized["startDate"],
                normalized["endDate"],
                normalized["percentage"],
            )
            return (
                jsonify(
                    {
                        "id": assignment_id,
                        "personId": normalized["personId"],
                        "projectId": normalized["projectId"],
                        "startDate": normalized["startDate"],
                        "endDate": normalized["endDate"],
                        "percentage": normalized["percentage"],
                    }
                ),
                201,
            )

        @app.route("/api/assignments/<int:assignment_id>", methods=["PUT"])
        def update_assignment(assignment_id: int):
            data = ValidationService.require_json({"personId", "projectId"})
            percentage = int(data.get("percentage", 100))

            if "startDate" in data and "endDate" in data:
                start_date = data["startDate"]
                end_date = data["endDate"]
            elif "period" in data:
                dates = ValidationService.convert_period_to_dates(int(data["period"]))
                start_date = dates["start"]
                end_date = dates["end"]
            else:
                abort(400, description="Either startDate/endDate or period is required")

            self.assignments_repo.update(
                assignment_id, data["personId"], data["projectId"], start_date, end_date, percentage
            )
            return (
                jsonify(
                    {
                        "id": assignment_id,
                        "personId": data["personId"],
                        "projectId": data["projectId"],
                        "startDate": start_date,
                        "endDate": end_date,
                        "percentage": percentage,
                    }
                ),
                200,
            )

        @app.route("/api/assignments/<int:assignment_id>", methods=["DELETE"])
        def delete_assignment(assignment_id: int):
            self.assignments_repo.delete(assignment_id)
            return jsonify({"success": True}), 200

        @app.route("/api/bulk-upload/people", methods=["POST"])
        def bulk_upload_people():
            data = ValidationService.require_json({"people"})
            added = self.bulk_service.bulk_people(data["people"])
            return jsonify({"added": added}), 201

        @app.route("/api/bulk-upload/clients", methods=["POST"])
        def bulk_upload_clients():
            data = ValidationService.require_json({"clients"})
            added = self.bulk_service.bulk_clients(data["clients"])
            return jsonify({"added": added}), 201

        @app.route("/api/bulk-upload/projects", methods=["POST"])
        def bulk_upload_projects():
            data = ValidationService.require_json({"projects"})
            try:
                added = self.bulk_service.bulk_projects(data["projects"])
            except ValueError as exc:
                abort(400, description=str(exc))
            return jsonify({"added": added}), 201

        @app.route("/api/bulk-upload/assignments", methods=["POST"])
        def bulk_upload_assignments():
            data = ValidationService.require_json({"assignments"})
            try:
                logger.info("Bulk upload assignments request: %s rows", len(data["assignments"]))
                added = []
                for row in data["assignments"]:
                    normalized = self._normalize_assignment_payload(row)
                    assignment_id = self.assignments_repo.find_existing(
                        normalized["personId"],
                        normalized["projectId"],
                        normalized["startDate"],
                        normalized["endDate"],
                    )
                    if assignment_id:
                        self.assignments_repo.update(
                            assignment_id,
                            normalized["personId"],
                            normalized["projectId"],
                            normalized["startDate"],
                            normalized["endDate"],
                            normalized["percentage"],
                        )
                    else:
                        assignment_id = self.assignments_repo.create(
                            normalized["personId"],
                            normalized["projectId"],
                            normalized["startDate"],
                            normalized["endDate"],
                            normalized["percentage"],
                        )
                    added.append(
                        {
                            "id": assignment_id,
                            "personId": normalized["personId"],
                            "projectId": normalized["projectId"],
                            "startDate": normalized["startDate"],
                            "endDate": normalized["endDate"],
                            "percentage": normalized["percentage"],
                        }
                    )
            except Exception as exc:
                logger.warning("Bulk upload assignments failed: %s", exc)
                abort(400, description=str(exc))
            return jsonify({"added": added}), 201

        @app.route("/api/clear-all", methods=["POST"])
        def clear_all():
            with self.connection_provider.get_connection() as conn:
                conn.execute("DELETE FROM assignments")
                conn.execute("DELETE FROM projects")
                conn.execute("DELETE FROM clients")
                conn.execute("DELETE FROM people")
            return jsonify({"success": True}), 200

        @app.route("/api/health", methods=["GET"])
        def health_check():
            return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200

    # ---------------------------- Lifecycle ---------------------------------
    def init_database(self) -> None:
        logger.info("Initializing database at %s", self.config.sqlite_path)
        self.db_initializer.initialize()

    def run(self) -> None:
        logger.info("🚀 Backend server starting...")
        logger.info("📊 Database: SQLite (%s)", self.config.sqlite_path)
        logger.info("🌐 API running on: http://localhost:5000")
        self.app.run(debug=False, host="0.0.0.0", port=5000)


config = DatabaseConfig()
api = ResourcePlannerAPI(config)
app = api.app

if __name__ == "__main__":
    api.init_database()
    api.run()
