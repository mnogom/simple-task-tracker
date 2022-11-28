USER_DATA = {
    'full_name': 'John Doe',
    'email': 'jd@google.com',
    'password': 'secret-password',
}

EXPECTED_USER = {
    'id': 1,
    'full_name': USER_DATA['full_name'],
    'email': USER_DATA['email'],
    'is_superuser': False,
    'is_active': True,
    'tasks': [],
}


def test_create_read_user(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == []

    response = client.post('/users/', json=USER_DATA)
    assert response.status_code == 200
    assert response.json() == EXPECTED_USER

    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == [EXPECTED_USER, ]

    response = client.get(f'/users/{EXPECTED_USER["id"]}')
    assert response.status_code == 200
    assert response.json() == EXPECTED_USER


def test_update_user(client):
    response = client.post('/users/', json=USER_DATA)
    user = response.json()
    updated_data = {'full_name': 'Serious Sam'}
    response = client.put(f'/users/{user["id"]}', json=updated_data)
    assert response.status_code == 200
    assert response.json() == {**EXPECTED_USER,
                               'full_name': updated_data['full_name']}


def test_remove_user(client):
    response = client.post('/users/', json=USER_DATA)
    user = response.json()
    response = client.delete(f'/users/{user["id"]}')
    assert response.status_code == 200
    assert response.json() == EXPECTED_USER

    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(f'/users/{EXPECTED_USER["id"]}')
    assert response.status_code == 404


def test_404(client):
    response = client.get('/users/1')
    assert response.status_code == 404

    response = client.put('/users/1', json=USER_DATA)
    assert response.status_code == 404

    response = client.delete('/users/1')
    assert response.status_code == 404