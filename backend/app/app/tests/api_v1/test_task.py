TASK = {
    'name': 'Test Task',
    'description': 'Some description of task'
}


def test_create_read_task(client, user):
    client.post('/users/', json=user)
    client.post('/tasks/', json=)

def test_update_task(client, user):

def test_delete_task(client, user):

def test_404(client, user):

