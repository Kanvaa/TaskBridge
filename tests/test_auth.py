import pytest
from models.user import User

def test_user_registration_and_login(client):
    # Test Registration
    response = client.post('/register', data={
        'username': 'tester',
        'email': 'tester@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Registration successful!" in response.data or b"Sign In" in response.data

    # Test Duplicate Registration
    response = client.post('/register', data={
        'username': 'tester',
        'email': 'tester2@example.com',
        'password': 'password123'
    })
    assert b"Username already exists." in response.data

    # Test Login
    response = client.post('/login', data={
        'username': 'tester',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged in successfully." in response.data
    assert b"Dashboard" in response.data

    # Test Logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged out successfully." in response.data
