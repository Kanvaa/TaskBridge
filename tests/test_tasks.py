import pytest
from models.user import User
from models.task import Task

@pytest.fixture
def logged_in_client(client):
    # Register & Login helper
    client.post('/register', data={
        'username': 'taskuser',
        'email': 'taskuser@example.com',
        'password': 'password123'
    })
    client.post('/login', data={
        'username': 'taskuser',
        'password': 'password123'
    })
    return client

def test_task_lifecycle(logged_in_client):
    # 1. Create task
    response = logged_in_client.post('/task/new', data={
        'title': 'Test Task Title',
        'description': 'Test Task Description',
        'status': 'Pending',
        'priority': 'High',
        'due_date': '2026-12-31'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Task created successfully!" in response.data
    assert b"Test Task Title" in response.data

    # Find the task in DB to get its ID
    user = User.find_by_username('taskuser')
    tasks = Task.find_by_user(user.id)
    assert len(tasks) >= 1
    task = tasks[0]
    assert task.title == 'Test Task Title'

    # 2. Edit task
    response = logged_in_client.post(f'/task/{task.id}/edit', data={
        'title': 'Updated Task Title',
        'description': 'Updated Task Description',
        'status': 'In Progress',
        'priority': 'Low',
        'due_date': '2026-12-31'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Task updated successfully!" in response.data
    assert b"Updated Task Title" in response.data

    # Verify updates in database
    updated_task = Task.find_by_id(task.id)
    assert updated_task.title == 'Updated Task Title'
    assert updated_task.status == 'In Progress'

    # 3. Filter tasks
    response = logged_in_client.get('/?status=In Progress')
    assert b"Updated Task Title" in response.data

    response = logged_in_client.get('/?status=Pending')
    assert b"Updated Task Title" not in response.data

    # 4. Delete task
    response = logged_in_client.post(f'/task/{task.id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"Task deleted successfully!" in response.data
    assert b"Updated Task Title" not in response.data
