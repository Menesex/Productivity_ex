from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Función para obtener una nueva conexión por cada request
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="productivity_ex",
        user="postgres",
        password="123"
    )

# -------------------- FOLDERS --------------------

@app.route('/folders', methods=['GET'])
def get_folders():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM folders")
            folders = cur.fetchall()
            return jsonify([
                {"id": f[0], "nombre": f[1]} for f in folders
            ])
    conn.close()

@app.route('/folders', methods=['POST'])
def add_folder():
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO folders (nombre) VALUES (%s) RETURNING id", (data['nombre'],))
            folder_id = cur.fetchone()[0]
            return jsonify({"id": folder_id})
    conn.close()

# -------------------- TASKS --------------------

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks")
            tasks = cur.fetchall()
            return jsonify([
                {
                    "id": t[0],
                    "titulo": t[1],
                    "descripcion": t[2],
                    "completada": t[3],
                    "folder_id": t[4]
                } for t in tasks
            ])
    conn.close()

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tasks (titulo, descripcion, completada, folder_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (
                data['titulo'],
                data.get('descripcion', ''),
                data.get('completada', False),
                data['folder_id']
            ))
            task_id = cur.fetchone()[0]
            return jsonify({"id": task_id})
    conn.close()

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE tasks
                SET completada = %s
                WHERE id = %s
            """, (data['completada'], task_id))
            return jsonify({"status": "ok"})
    conn.close()

# -------------------- RUN APP --------------------

if __name__ == '__main__':
    app.run(debug=True)
