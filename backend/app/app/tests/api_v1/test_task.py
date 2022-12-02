from app.tests.utils.user import create_test_user

TASK = {
    'name': 'Test Task',
    'deadline': '2022-01-01',
    'description': 'Some description of task'
}


def test_create_read_task(client, db):
    user = create_test_user(db=db)
    response = client.get('/tasks/')
    assert response.json() == []

    response = client.post('/tasks/', json=TASK)
    response_json = response.json()
    assert response_json.get('name') == TASK['name']
    assert response_json.get('deadline') == TASK['deadline']
    assert response_json.get('description') == TASK['description']
    assert response_json.get('id') == 1
    assert response_json.get('owner_id') == user.id
    assert 'created_at' in response_json

    response = client.get('/tasks/')
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get('/tasks/1/')
    assert response.status_code == 200


def test_update_task(client, db):
    user = create_test_user(db=db)

    client.post('/tasks/', json=TASK)
    new_name = 'Updated task name'
    new_created_at = '1990-01-01'
    response = client.put('/tasks/1/', json={'name': new_name,
                                             'created_at': new_created_at})
    response_json = response.json()
    assert response_json.get('name') == new_name
    assert response_json.get('deadline') == TASK['deadline']
    assert response_json.get('description') == TASK['description']
    assert response_json.get('id') == 1
    assert response_json.get('owner_id') == user.id
    assert response_json.get('created_at') != new_created_at


def test_delete_task(client, db):
    user = create_test_user(db=db)
    client.post('/tasks/', json=TASK)
    response = client.delete('/tasks/1/')
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get('name') == TASK['name']
    assert response_json.get('deadline') == TASK['deadline']
    assert response_json.get('description') == TASK['description']
    assert response_json.get('id') == 1
    assert response_json.get('owner_id') == user.id
    assert 'created_at' in response_json

    response = client.get('/tasks/')
    assert response.json() == []


def test_404(client):
    response = client.get('/users/1/')
    assert response.status_code == 404

    response = client.put('/users/1', json={'name': '123'})
    assert response.status_code == 404

    response = client.delete('/users/1/')
    assert response.status_code == 404
