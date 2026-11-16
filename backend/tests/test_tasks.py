def test_create_task_without_due_date(client):
    register_response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert register_response.status_code == 200

    user_id = register_response.json()["id"]

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

    project_response = client.post(
        "/projects/",
        json={
            "project_name": "Test Project"
        },
        headers=headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        "/tasks/",
        json={
            "name": "Test Task",
            "project_id": project_id,
            "assigned_user_id": user_id
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Task"
    assert data["project_id"] == project_id
    assert data["user_id"] == user_id
    assert data["status"] == "TODO"
    assert data["due_date"] is None
    assert "id" in data
    
    
    
def test_create_task_with_due_date(client):
    register_response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert register_response.status_code == 200

    user_id = register_response.json()["id"]

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

    project_response = client.post(
        "/projects/",
        json={
            "project_name": "Test Project"
        },
        headers=headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        "/tasks/",
        json={
            "name": "Test Task With Due Date",
            "project_id": project_id,
            "assigned_user_id": user_id,
            "status": "TODO",
            "due_date": "2030-12-31"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Task With Due Date"
    assert data["project_id"] == project_id
    assert data["user_id"] == user_id
    assert data["status"] == "TODO"
    assert data["due_date"] == "2030-12-31"
    assert "id" in data
        
        
def test_remove_task_due_date(client):
    register_response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert register_response.status_code == 200

    user_id = register_response.json()["id"]

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

    project_response = client.post(
        "/projects/",
        json={
            "project_name": "Test Project"
        },
        headers=headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    task_response = client.post(
        "/tasks/",
        json={
            "name": "Test Task",
            "project_id": project_id,
            "assigned_user_id": user_id,
            "due_date": "2030-12-31"
        },
        headers=headers
    )

    assert task_response.status_code == 200
    assert task_response.json()["due_date"] == "2030-12-31"

    task_id = task_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "due_date": None
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["due_date"] is None

    tasks_response = client.get(
        "/tasks/",
        params={"project_id": project_id},
        headers=headers
    )

    assert tasks_response.status_code == 200

    tasks = tasks_response.json()

    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["due_date"] is None
    assert tasks[0]["user_id"] == user_id        



def test_update_task_due_date(client):
    register_response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert register_response.status_code == 200

    user_id = register_response.json()["id"]

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

    project_response = client.post(
        "/projects/",
        json={
            "project_name": "Test Project"
        },
        headers=headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    task_response = client.post(
        "/tasks/",
        json={
            "name": "Test Task",
            "project_id": project_id,
            "assigned_user_id": user_id
        },
        headers=headers
    )

    assert task_response.status_code == 200
    assert task_response.json()["due_date"] is None

    task_id = task_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"due_date": "2030-12-31"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == "2030-12-31"

    response = client.put(
        f"/tasks/{task_id}",
        json={"due_date": "2031-01-15"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == "2031-01-15"

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "IN_PROGRESS"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"
    assert response.json()["due_date"] == "2031-01-15"
    assert response.json()["user_id"] == user_id

    tasks_response = client.get(
        "/tasks/",
        params={"project_id": project_id},
        headers=headers
    )

    assert tasks_response.status_code == 200

    tasks = tasks_response.json()

    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["due_date"] == "2031-01-15"
    assert tasks[0]["status"] == "IN_PROGRESS"
    assert tasks[0]["user_id"] == user_id



def test_unauthorized_task_access(client):
    owner_response = client.post(
        "/users/",
        json={
            "username": "project_owner",
            "email": "owner@example.com",
            "password": "TestPassword123!"
        }
    )

    assert owner_response.status_code == 200

    owner_id = owner_response.json()["id"]

    other_response = client.post(
        "/users/",
        json={
            "username": "other_user",
            "email": "other@example.com",
            "password": "TestPassword123!"
        }
    )

    assert other_response.status_code == 200

    other_id = other_response.json()["id"]

    owner_login = client.post(
        "/users/login",
        data={
            "username": "project_owner",
            "password": "TestPassword123!"
        }
    )

    assert owner_login.status_code == 200

    owner_headers = {
        "Authorization": f"Bearer {owner_login.json()['access_token']}"
    }

    other_login = client.post(
        "/users/login",
        data={
            "username": "other_user",
            "password": "TestPassword123!"
        }
    )

    assert other_login.status_code == 200

    other_headers = {
        "Authorization": f"Bearer {other_login.json()['access_token']}"
    }

    project_response = client.post(
        "/projects/",
        json={"project_name": "Private Project"},
        headers=owner_headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    task_response = client.post(
        "/tasks/",
        json={
            "name": "Private Task",
            "project_id": project_id,
            "assigned_user_id": owner_id
        },
        headers=owner_headers
    )

    assert task_response.status_code == 200

    task_id = task_response.json()["id"]

    response = client.get(
        "/tasks/",
        params={"project_id": project_id},
        headers=other_headers
    )

    assert response.status_code == 200
    assert response.json() == []

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "DONE"},
        headers=other_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

    response = client.delete(
        f"/tasks/{task_id}",
        headers=other_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

    response = client.post(
        "/tasks/",
        json={
            "name": "Unauthorized Task",
            "project_id": project_id,
            "assigned_user_id": other_id
        },
        headers=other_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "User does not own this project"
    )

    response = client.get(
        "/tasks/",
        params={"project_id": project_id},
        headers=owner_headers
    )

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["name"] == "Private Task"
    assert tasks[0]["status"] == "TODO"
    assert tasks[0]["user_id"] == owner_id            
    
    

def test_task_assignment_permissions(client):
    user_ids = {}
    user_headers = {}

    for username in ["project_owner", "assigned_user", "third_user"]:
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
    third_headers = user_headers["third_user"]

    assigned_id = user_ids["assigned_user"]
    third_id = user_ids["third_user"]

    project_response = client.post(
        "/projects/",
        json={"project_name": "Assignment Test Project"},
        headers=owner_headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    task_response = client.post(
        "/tasks/",
        json={
            "name": "Assigned Task",
            "project_id": project_id,
            "assigned_user_id": assigned_id
        },
        headers=owner_headers
    )

    assert task_response.status_code == 200
    assert task_response.json()["user_id"] == assigned_id

    task_id = task_response.json()["id"]

    response = client.get(
        "/projects/",
        headers=assigned_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == project_id

    response = client.get(
        "/tasks/",
        params={"project_id": project_id},
        headers=assigned_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == task_id

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "IN_PROGRESS"},
        headers=assigned_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"
    assert response.json()["user_id"] == assigned_id

    response = client.put(
        f"/tasks/{task_id}",
        json={"assigned_user_id": third_id},
        headers=assigned_headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Only the project owner can reassign tasks"
    )

    response = client.delete(
        f"/tasks/{task_id}",
        headers=assigned_headers
    )

    assert response.status_code == 404

    response = client.get(
        "/tasks/",
        params={"project_id": project_id},
        headers=owner_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == assigned_id

    response = client.put(
        f"/tasks/{task_id}",
        json={"assigned_user_id": third_id},
        headers=owner_headers
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == third_id
    assert response.json()["status"] == "IN_PROGRESS"

    response = client.get(
        "/tasks/",
        params={"project_id": project_id},
        headers=assigned_headers
    )

    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        "/tasks/",
        params={"project_id": project_id},
        headers=third_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == task_id
    assert response.json()[0]["user_id"] == third_id
        