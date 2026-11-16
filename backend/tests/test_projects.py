from database.database import SessionLocal
from models.project import Project
from models.task import Task
from models.comment import Comment


def test_project_cascade_deletion(client):
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
        json={"project_name": "Cascade Test Project"},
        headers=headers
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    task_ids = []
    comment_ids = []

    for i in range(2):
        task_response = client.post(
            "/tasks/",
            json={
                "name": f"Task {i + 1}",
                "project_id": project_id,
                "assigned_user_id": user_id
            },
            headers=headers
        )

        assert task_response.status_code == 200

        task_id = task_response.json()["id"]
        task_ids.append(task_id)

        for j in range(2):
            comment_response = client.post(
                "/comments/",
                params={"task_id": task_id},
                json={"content": f"Comment {j + 1}"},
                headers=headers
            )

            assert comment_response.status_code == 200

            comment_ids.append(
                comment_response.json()["id"]
            )

    with SessionLocal() as db:
        assert db.query(Project).count() == 1
        assert db.query(Task).count() == 2
        assert db.query(Comment).count() == 4

    # Delete project
    response = client.delete(
        f"/projects/{project_id}",
        headers=headers
    )

    assert response.status_code == 200

    assert response.json()["message"] == (
        "Project deleted successfully"
    )

    with SessionLocal() as db:
        assert db.get(Project, project_id) is None

        for task_id in task_ids:
            assert db.get(Task, task_id) is None

        for comment_id in comment_ids:
            assert db.get(Comment, comment_id) is None

        assert db.query(Project).count() == 0
        assert db.query(Task).count() == 0
        assert db.query(Comment).count() == 0
        
        
def test_unauthorized_project_access(client):
    owner_response = client.post(
        "/users/",
        json={
            "username": "project_owner",
            "email": "owner@example.com",
            "password": "TestPassword123!"
        }
    )

    assert owner_response.status_code == 200

    other_response = client.post(
        "/users/",
        json={
            "username": "other_user",
            "email": "other@example.com",
            "password": "TestPassword123!"
        }
    )

    assert other_response.status_code == 200

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

    response = client.get(
        "/projects/",
        headers=other_headers
    )

    assert response.status_code == 200
    assert response.json() == []

    response = client.put(
        f"/projects/{project_id}",
        json={"project_name": "Unauthorized Update"},
        headers=other_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"

    response = client.delete(
        f"/projects/{project_id}",
        headers=other_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"

    response = client.get(
        "/projects/",
        headers=owner_headers
    )

    assert response.status_code == 200

    projects = response.json()

    assert len(projects) == 1
    assert projects[0]["id"] == project_id
    assert projects[0]["project_name"] == "Private Project"
    
    
            