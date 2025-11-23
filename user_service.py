from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
USERS_DB = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    # Agregamos campo password
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT, role TEXT)')
    
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Creamos un Admin y un Cliente
        users = [
            ('admin', 'admin@tienda.com', '1234', 'admin'),
            ('juan', 'juan@gmail.com', '1234', 'cliente')
        ]
        cursor.executemany("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", users)
        conn.commit()
    conn.close()

# 1. Registro
@app.route('/users/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", 
                       (data['username'], data['email'], data['password'], 'cliente'))
        conn.commit()
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

# 2. Autenticación (Login)
@app.route('/users/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    # En vida real, usaríamos Hash para passwords
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                        (data['username'], data['password'])).fetchone()
    conn.close()
    
    if user:
        return jsonify({
            "id": user['id'], 
            "username": user['username'], 
            "email": user['email'],
            "role": user['role']
        }), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    init_db()
    print("Iniciando Servicio de Usuarios (Auth) en puerto 5001...")
    app.run(port=5001, host='0.0.0.0')
