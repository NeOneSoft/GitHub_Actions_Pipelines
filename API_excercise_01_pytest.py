import json
from API_excercise_01 import app

def test_get_user():
    client = app.test_client()
    response = client.get('/users/1')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data['id'] == 1
    assert data['name'] == 'John Doe'
    assert data['email'] == 'johndoe@example.com'

def test_get_user_not_found():
    client = app.test_client()
    response = client.get('/users/999')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 404
    assert data['message'] == 'Usuario no encontrado'

def test_create_user():
    client = app.test_client()
    data = {
        'name': 'Jane Smith',
        'email': 'janesmith@example.com'
    }
    headers = {'Content-Type': 'application/json'}
    response = client.post('/users', headers=headers, data=json.dumps(data))
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data['message'] == 'Usuario creado exitosamente'
    assert data['id'] is not None

