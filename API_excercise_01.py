from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Endpoint para obtener información de un usuario por su ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Establecer conexión con la base de datos
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Obtener información del usuario desde la base de datos
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()

    if user is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Convertir la información del usuario en un diccionario
    user_data = {
        'id': user[0],
        'name': user[1],
        'email': user[2]
    }

    return jsonify(user_data)

# Endpoint para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    # Obtener los datos del nuevo usuario desde el cuerpo de la solicitud
    data = request.get_json()
    name = data['name']
    email = data['email']

    # Establecer conexión con la base de datos
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insertar los datos del nuevo usuario en la base de datos
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()

    # Obtener el ID del nuevo usuario
    user_id = cursor.lastrowid

    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()

    # Devolver una respuesta exitosa con el ID del nuevo usuario
    return jsonify({'message': 'Usuario creado exitosamente', 'id': user_id})

if __name__ == '__main__':
    # Crear la tabla de usuarios en la base de datos (solo para propósitos de ejemplo)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
        )
    ''')

    cursor.close()
    conn.close()

    # Ejecutar la aplicación Flask
    app.run()

'''
Curl:
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "Alfredo Romero",
  "email": "alfredoromero@example.com"
}' http://localhost:5000/users

curl -X GET http://localhost:5000/users/1

'''
