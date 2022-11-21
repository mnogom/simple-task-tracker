def test_create_user(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == []

    full_name = 'John Doe'
    email = 'jd@google.com'
    password = 'secret-password'
    data = {
        'full_name': full_name,
        'email': email,
        'password': password,
    }
    response = client.post('/users/', json=data)
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'full_name': full_name,
        'email': email,
        'is_superuser': False,
        'is_active': True,
        'tasks': [],
    }

    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == [{
        'id': 1,
        'full_name': full_name,
        'email': email,
        'is_superuser': False,
        'is_active': True,
        'tasks': [],
    }]


def test_tests(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == []
