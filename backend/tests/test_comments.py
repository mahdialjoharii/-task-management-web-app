def test_comment_editing_permissions(client):
    user_ids = {}
    user_headers = {}

    for username in ["project_owner", "assigned_user", "other_user"]:
        register_response = client.post(
            "/users/",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": "TestPassword123!"
            }
        )

        assert register_response.status_code == 200

        user_ids[username] = register_response.json()["id"]

        login_response = client.post(
            "/users/login",
            data={
                "username": username,
                "password": "TestPassword123!"
            }
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        user_headers[username] = {
            "Authorization": f"Bearer {token}"
        }

    owner_headers = user_headers["project_owner"]
    assigned_headers = user_headers["assigned_user"]
    other_headers = user_headers["other_user"]

    assigned_id = user_ids["assigned_user"]

    project_response = client.post(
        "/projects/",
        json={"project_name": "Comment Test Project"},
        headers=owner_headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    task_response = client.post(
        "/tasks/",
        json={
            "name": "Comment Test Task",
            "project_id": project_id,
            "assigned_user_id": assigned_id
        },
        headers=owner_headers
    )

    assert task_response.status_code == 200

    task_id = task_response.json()["id"]

    comment_response = client.post(
        "/comments/",
        params={"task_id": task_id},
        json={"content": "Original Comment"},
        headers=assigned_headers
    )

    assert comment_response.status_code == 200

    comment_id = comment_response.json()["id"]

    assert comment_response.json()["user_id"] == assigned_id

    response = client.put(
        f"/comments/{comment_id}",
        json={"content": "Updated Comment"},
        headers=assigned_headers
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Updated Comment"

    response = client.put(
        f"/comments/{comment_id}",
        json={"content": "Owner Unauthorized Update"},
        headers=owner_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Comment not found"

    response = client.put(
        f"/comments/{comment_id}",
        json={"content": "Unauthorized Update"},
        headers=other_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Comment not found"

    response = client.get(
        "/comments/",
        params={"task_id": task_id},
        headers=owner_headers
    )

    assert response.status_code == 200

    comments = response.json()

    assert len(comments) == 1
    assert comments[0]["id"] == comment_id
    assert comments[0]["content"] == "Updated Comment"
    assert comments[0]["user_id"] == assigned_id
    
    
    
def test_comment_deletion_permissions(client):
    user_ids = {}
    user_headers = {}

    for username in ["project_owner", "assigned_user", "other_user"]:
        register_response = client.post(
            "/users/",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": "TestPassword123!"
            }
        )

        assert register_response.status_code == 200

        user_ids[username] = register_response.json()["id"]

        login_response = client.post(
            "/users/login",
            data={
                "username": username,
                "password": "TestPassword123!"
            }
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        user_headers[username] = {
            "Authorization": f"Bearer {token}"
        }

    owner_headers = user_headers["project_owner"]
    assigned_headers = user_headers["assigned_user"]
    other_headers = user_headers["other_user"]

    assigned_id = user_ids["assigned_user"]

    project_response = client.post(
        "/projects/",
        json={"project_name": "Comment Deletion Project"},
        headers=owner_headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    task_response = client.post(
        "/tasks/",
        json={
            "name": "Comment Deletion Task",
            "project_id": project_id,
            "assigned_user_id": assigned_id
        },
        headers=owner_headers
    )

    assert task_response.status_code == 200

    task_id = task_response.json()["id"]

    comment_ids = []

    for i in range(2):
        comment_response = client.post(
            "/comments/",
            params={"task_id": task_id},
            json={"content": f"Comment {i + 1}"},
            headers=assigned_headers
        )

        assert comment_response.status_code == 200

        comment_ids.append(comment_response.json()["id"])

    response = client.delete(
        f"/comments/{comment_ids[0]}",
        headers=other_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Comment not found"

    response = client.get(
        "/comments/",
        params={"task_id": task_id},
        headers=owner_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.delete(
        f"/comments/{comment_ids[0]}",
        headers=assigned_headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Comment deleted successfully"

    response = client.get(
        "/comments/",
        params={"task_id": task_id},
        headers=owner_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == comment_ids[1]

    response = client.delete(
        f"/comments/{comment_ids[1]}",
        headers=owner_headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Comment deleted successfully"

    response = client.get(
        "/comments/",
        params={"task_id": task_id},
        headers=owner_headers
    )

    assert response.status_code == 200
    assert response.json() == []    
    
    
    
def test_comment_access_permissions(client):
    user_ids = {}
    user_headers = {}

    for username in ["project_owner", "assigned_user", "other_user"]:
        register_response = client.post(
            "/users/",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": "TestPassword123!"
            }
        )

        assert register_response.status_code == 200

        user_ids[username] = register_response.json()["id"]

        login_response = client.post(
            "/users/login",
            data={
                "username": username,
                "password": "TestPassword123!"
            }
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        user_headers[username] = {
            "Authorization": f"Bearer {token}"
        }

    owner_headers = user_headers["project_owner"]
    assigned_headers = user_headers["assigned_user"]
    other_headers = user_headers["other_user"]

    owner_id = user_ids["project_owner"]
    assigned_id = user_ids["assigned_user"]

    project_response = client.post(
        "/projects/",
        json={"project_name": "Comment Access Project"},
        headers=owner_headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    task_response = client.post(
        "/tasks/",
        json={
            "name": "Comment Access Task",
            "project_id": project_id,
            "assigned_user_id": assigned_id
        },
        headers=owner_headers
    )

    assert task_response.status_code == 200

    task_id = task_response.json()["id"]

    response = client.post(
        "/comments/",
        params={"task_id": task_id},
        json={"content": "Owner Comment"},
        headers=owner_headers
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == owner_id

    response = client.post(
        "/comments/",
        params={"task_id": task_id},
        json={"content": "Assigned User Comment"},
        headers=assigned_headers
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == assigned_id

    response = client.get(
        "/comments/",
        params={"task_id": task_id},
        headers=other_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

    response = client.post(
        "/comments/",
        params={"task_id": task_id},
        json={"content": "Unauthorized Comment"},
        headers=other_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

    for headers in [owner_headers, assigned_headers]:
        response = client.get(
            "/comments/",
            params={"task_id": task_id},
            headers=headers
        )

        assert response.status_code == 200

        comments = response.json()

        assert len(comments) == 2

        assert {c["content"] for c in comments} == {
            "Owner Comment",
            "Assigned User Comment"
        }    