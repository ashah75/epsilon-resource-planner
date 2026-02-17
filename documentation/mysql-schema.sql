-- MySQL schema for epsilon-resource-planner

CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    client_id INT NOT NULL,
    CONSTRAINT fk_projects_client
        FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    project_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    percentage INT DEFAULT 100,
    CONSTRAINT fk_assignments_person
        FOREIGN KEY (person_id) REFERENCES people(id),
    CONSTRAINT fk_assignments_project
        FOREIGN KEY (project_id) REFERENCES projects(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_assignments_person ON assignments(person_id);
CREATE INDEX idx_assignments_project ON assignments(project_id);
