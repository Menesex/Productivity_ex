from flask import Flask, jsonify, request
from flask_cors import CORS
from db_config import get_db_connection

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'API funcionando correctamente'

# Obtener todas las listas
@app.route('/listas', methods=['GET'])
def get_listas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, titulo, created_at FROM listas ORDER BY created_at DESC')
    listas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {"id": l[0], "titulo": l[1], "created_at": l[2].isoformat()} for l in listas
    ])

# Obtener tareas de una lista específica
@app.route('/tareas/<id_lista>', methods=['GET'])
def get_tareas(id_lista):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT id, titulo, descripcion, hecha, created_at FROM tareas WHERE id_lista = %s ORDER BY created_at DESC',
        (id_lista,)
    )
    tareas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {"id": t[0], "titulo": t[1], "descripcion": t[2], "hecha": t[3], "created_at": t[4].isoformat()} for t in tareas
    ])

# Agregar una tarea nueva
@app.route('/tareas', methods=['POST'])
def add_tarea():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO tareas (id_lista, titulo, descripcion, hecha) VALUES (%s, %s, %s, %s) RETURNING id',
        (data['id_lista'], data['titulo'], data['descripcion'], False)
    )
    tarea_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Tarea creada", "id": tarea_id})

# Marcar tarea como hecha
@app.route('/tareas/<id>', methods=['PUT'])
def marcar_hecha(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tareas SET hecha = TRUE WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Tarea marcada como hecha"})

if __name__ == '__main__':
    app.run(debug=True)
