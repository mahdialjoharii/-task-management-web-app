from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import jwt
from auth import SECRET_KEY, ALGORITHM


def test_register_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "test_user"
    assert data["email"] == "test_user@example.com"
    assert "id" in data
    assert "password" not in data
    
    
def test_login_success(client):
    register_response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "TestPassword123!"
        }
    )

    assert register_response.status_code == 200

    response = client.post(
        "/users/login",
        data={
            "username": "test_user",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"    
    
    
def test_login_wrong_password(client):
    register_response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "TestPassword123!"
        }
    )

    assert register_response.status_code == 200

    response = client.post(
        "/users/login",
        data={
            "username": "test_user",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid username or password"
    assert "access_token" not in data    
    
    
def test_login_nonexistent_user(client):
    response = client.post(
        "/users/login",
        data={
            "username": "nonexistent_user",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid username or password"
    assert "access_token" not in data    
    
    
def test_protected_endpoint_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"    
    
    
def test_expired_token(client):
    expired_token = jwt.encode(
        {
            "user_id": 1,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {expired_token}"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"    
    
    
def test_revoked_token(client):
    register_response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "TestPassword123!"
        }
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/users/login",
        data={
            "username": "test_user",
            "password": "TestPassword123!"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response_before = client.get(
        "/users/me",
        headers=headers
    )

    assert response_before.status_code == 200

    logout_response = client.post(
        "/users/logout",
        headers=headers
    )

    assert logout_response.status_code == 200

    response_after = client.get(
        "/users/me",
        headers=headers
    )

    assert response_after.status_code == 401
    assert response_after.json()["detail"] == "Token has been revoked"    
    