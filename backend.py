from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

DATABASE = 'resource_planner.db'

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS people
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  role TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS clients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS projects
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  client_id INTEGER NOT NULL,
                  FOREIGN KEY (client_id) REFERENCES clients(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS assignments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  person_id INTEGER NOT NULL,
                  project_id INTEGER NOT NULL,
                  start_date TEXT NOT NULL,
                  end_date TEXT NOT NULL,
                  percentage INTEGER DEFAULT 100,
                  FOREIGN KEY (person_id) REFERENCES people(id),
                  FOREIGN KEY (project_id) REFERENCES projects(id))''')
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ============= PEOPLE ENDPOINTS =============

@app.route('/api/people', methods=['GET'])
def get_people():
    conn = get_db()
    people = conn.execute('SELECT * FROM people').fetchall()
    conn.close()
    return jsonify([dict(p) for p in people])

@app.route('/api/people', methods=['POST'])
def add_person():
    data = request.json
    conn = get_db()
    cursor = conn.execute('INSERT INTO people (name, role) VALUES (?, ?)',
                         (data['name'], data['role']))
    conn.commit()
    person_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': person_id, 'name': data['name'], 'role': data['role']}), 201

@app.route('/api/people/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    conn = get_db()
    # Delete associated assignments first
    conn.execute('DELETE FROM assignments WHERE person_id = ?', (person_id,))
    # Delete person
    conn.execute('DELETE FROM people WHERE id = ?', (person_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

@app.route('/api/people/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.json
    conn = get_db()
    conn.execute('UPDATE people SET name = ?, role = ? WHERE id = ?', 
                 (data['name'], data['role'], person_id))
    conn.commit()
    conn.close()
    return jsonify({'id': person_id, 'name': data['name'], 'role': data['role']}), 200

# ============= CLIENTS ENDPOINTS =============

@app.route('/api/clients', methods=['GET'])
def get_clients():
    conn = get_db()
    clients = conn.execute('SELECT * FROM clients').fetchall()
    conn.close()
    return jsonify([dict(c) for c in clients])

@app.route('/api/clients', methods=['POST'])
def add_client():
    data = request.json
    conn = get_db()
    cursor = conn.execute('INSERT INTO clients (name) VALUES (?)', (data['name'],))
    conn.commit()
    client_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': client_id, 'name': data['name']}), 201

@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    conn = get_db()
    # Get all projects for this client
    projects = conn.execute('SELECT id FROM projects WHERE client_id = ?', (client_id,)).fetchall()
    project_ids = [p['id'] for p in projects]
    
    # Delete assignments for these projects
    for project_id in project_ids:
        conn.execute('DELETE FROM assignments WHERE project_id = ?', (project_id,))
    
    # Delete projects
    conn.execute('DELETE FROM projects WHERE client_id = ?', (client_id,))
    
    # Delete client
    conn.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

@app.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.json
    conn = get_db()
    conn.execute('UPDATE clients SET name = ? WHERE id = ?', 
                 (data['name'], client_id))
    conn.commit()
    conn.close()
    return jsonify({'id': client_id, 'name': data['name']}), 200

# ============= PROJECTS ENDPOINTS =============

@app.route('/api/projects', methods=['GET'])
def get_projects():
    conn = get_db()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return jsonify([dict(p) for p in projects])

@app.route('/api/projects', methods=['POST'])
def add_project():
    data = request.json
    conn = get_db()
    cursor = conn.execute('INSERT INTO projects (name, client_id) VALUES (?, ?)',
                         (data['name'], data['clientId']))
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': project_id, 'name': data['name'], 'clientId': data['clientId']}), 201

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    conn = get_db()
    # Delete assignments for this project
    conn.execute('DELETE FROM assignments WHERE project_id = ?', (project_id,))
    # Delete project
    conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    conn = get_db()
    conn.execute('UPDATE projects SET name = ?, client_id = ? WHERE id = ?', 
                 (data['name'], data['clientId'], project_id))
    conn.commit()
    conn.close()
    return jsonify({'id': project_id, 'name': data['name'], 'clientId': data['clientId']}), 200

# ============= ASSIGNMENTS ENDPOINTS =============

@app.route('/api/assignments', methods=['GET'])
def get_assignments():
    conn = get_db()
    assignments = conn.execute('SELECT * FROM assignments').fetchall()
    conn.close()
    return jsonify([dict(a) for a in assignments])

@app.route('/api/assignments', methods=['POST'])
def add_assignment():
    data = request.json
    percentage = data.get('percentage', 100)
    
    # Handle both old format (period) and new format (startDate/endDate)
    if 'startDate' in data and 'endDate' in data:
        # New date-based format
        start_date = data['startDate']
        end_date = data['endDate']
    elif 'period' in data:
        # Old period-based format - convert to dates
        period = data['period']
        # Calculate dates from period (each period is 14 days starting Jan 1, 2026)
        from datetime import datetime, timedelta
        base_date = datetime(2026, 1, 1)
        period_start = base_date + timedelta(days=period * 14)
        period_end = period_start + timedelta(days=13)
        start_date = period_start.strftime('%Y-%m-%d')
        end_date = period_end.strftime('%Y-%m-%d')
    else:
        return jsonify({'error': 'Either startDate/endDate or period is required'}), 400
    
    conn = get_db()
    cursor = conn.execute('INSERT INTO assignments (person_id, project_id, start_date, end_date, percentage) VALUES (?, ?, ?, ?, ?)',
                         (data['personId'], data['projectId'], start_date, end_date, percentage))
    conn.commit()
    assignment_id = cursor.lastrowid
    conn.close()
    return jsonify({
        'id': assignment_id,
        'personId': data['personId'],
        'projectId': data['projectId'],
        'startDate': start_date,
        'endDate': end_date,
        'percentage': percentage
    }), 201

@app.route('/api/assignments/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    conn = get_db()
    conn.execute('DELETE FROM assignments WHERE id = ?', (assignment_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

# ============= BULK UPLOAD ENDPOINTS =============

@app.route('/api/bulk-upload/people', methods=['POST'])
def bulk_upload_people():
    data = request.json
    conn = get_db()
    added = []
    for person in data['people']:
        cursor = conn.execute('INSERT INTO people (name, role) VALUES (?, ?)',
                            (person['name'], person['role']))
        added.append({'id': cursor.lastrowid, 'name': person['name'], 'role': person['role']})
    conn.commit()
    conn.close()
    return jsonify({'added': added}), 201

@app.route('/api/bulk-upload/clients', methods=['POST'])
def bulk_upload_clients():
    data = request.json
    conn = get_db()
    added = []
    for client in data['clients']:
        cursor = conn.execute('INSERT INTO clients (name) VALUES (?)', (client['name'],))
        added.append({'id': cursor.lastrowid, 'name': client['name']})
    conn.commit()
    conn.close()
    return jsonify({'added': added}), 201

@app.route('/api/bulk-upload/projects', methods=['POST'])
def bulk_upload_projects():
    data = request.json
    conn = get_db()
    added = []
    for project in data['projects']:
        cursor = conn.execute('INSERT INTO projects (name, client_id) VALUES (?, ?)',
                            (project['name'], project['clientId']))
        added.append({'id': cursor.lastrowid, 'name': project['name'], 'clientId': project['clientId']})
    conn.commit()
    conn.close()
    return jsonify({'added': added}), 201

@app.route('/api/bulk-upload/assignments', methods=['POST'])
def bulk_upload_assignments():
    data = request.json
    conn = get_db()
    added = []
    for assignment in data['assignments']:
        percentage = assignment.get('percentage', 100)
        cursor = conn.execute('INSERT INTO assignments (person_id, project_id, start_date, end_date, percentage) VALUES (?, ?, ?, ?, ?)',
                            (assignment['personId'], assignment['projectId'], assignment['startDate'], assignment['endDate'], percentage))
        added.append({
            'id': cursor.lastrowid,
            'personId': assignment['personId'],
            'projectId': assignment['projectId'],
            'startDate': assignment['startDate'],
            'endDate': assignment['endDate'],
            'percentage': percentage
        })
    conn.commit()
    conn.close()
    return jsonify({'added': added}), 201

# ============= UTILITY ENDPOINTS =============

@app.route('/api/clear-all', methods=['POST'])
def clear_all():
    """Clear all data from the database"""
    conn = get_db()
    conn.execute('DELETE FROM assignments')
    conn.execute('DELETE FROM projects')
    conn.execute('DELETE FROM clients')
    conn.execute('DELETE FROM people')
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    init_db()
    print("🚀 Backend server starting...")
    print("📊 Database: SQLite (resource_planner.db)")
    print("🌐 API running on: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
