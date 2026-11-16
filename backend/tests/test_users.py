import pytest


@pytest.mark.parametrize(
    "username, email, password",
    [
        ("ab", "test@example.com", "TestPassword123!"),
        ("   ", "test@example.com", "TestPassword123!"),
        ("test_user", "invalid-email", "TestPassword123!"),
        ("test_user", "test@example.com", "123"),
        ("test_user", "test@example.com", "        "),
        ("test_user", "test@example.com", "a" * 73),
        ("a" * 31, "test@example.com", "TestPassword123!"),
    ]
)
def test_invalid_registration(client, username, email, password):
    response = client.post(
        "/users/",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 422
    
    
    
def test_user_privacy(client):
    first_user = client.post(
        "/users/",
        json={
            "username": "first_user",
            "email": "first@example.com",
            "password": "TestPassword123!"
        }
    )

    assert first_user.status_code == 200

    second_user = client.post(
        "/users/",
        json={
            "username": "second_user",
            "email": "second@example.com",
            "password": "TestPassword123!"
        }
    )

    assert second_user.status_code == 200

    login_response = client.post(
        "/users/login",
        data={
            "username": "first_user",
            "password": "TestPassword123!"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 2

    for user in users:
        assert "id" in user
        assert "username" in user
        assert "email" not in user
        assert "password" not in user
        assert set(user.keys()) == {"id", "username"}    