from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import task, project, user
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from auth import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    existing_project = db.query(project.Project).filter(
    project.Project.id == task_data.project_id
).first()

    if existing_project is None:
     raise HTTPException(
        status_code=400,
        detail="Project does not exist"
    )
    assigned_user = db.query(user.User).filter(
    user.User.id == task_data.assigned_user_id
).first()

    if assigned_user is None:
     raise HTTPException(
        status_code=400,
        detail="Assigned user does not exist"
    )
    if existing_project.user_id != user_id:
       raise HTTPException(
        status_code=400,
        detail="User does not own this project"
    )
    new_task = task.Task(
        name=task_data.name,
        project_id=task_data.project_id,
       user_id=task_data.assigned_user_id,
        status=task_data.status,
        due_date=task_data.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    status: str | None = None,
    project_id: int | None = None,
    name: str | None = None,
    sort_by_due_date: bool = False,
    sort_desc: bool = False,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    owned_project_ids = db.query(project.Project.id).filter(
    project.Project.user_id == user_id
).subquery()

    tasks_query = db.query(task.Task).filter(
      (task.Task.user_id == user_id) |
      (task.Task.project_id.in_(owned_project_ids))
)

    if status is not None:
        tasks_query = tasks_query.filter(
            task.Task.status == status
        )

    if project_id is not None:
        tasks_query = tasks_query.filter(
            task.Task.project_id == project_id
        )

    if name is not None:
        tasks_query = tasks_query.filter(
            task.Task.name.contains(name)
        )

    if sort_by_due_date:
     if sort_desc:
        tasks_query = tasks_query.order_by(
            task.Task.due_date.desc()
        )
     else:
        tasks_query = tasks_query.order_by(
            task.Task.due_date.asc()
        )
    return tasks_query.all()


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    existing_task = db.query(task.Task).join(
     project.Project,
     task.Task.project_id == project.Project.id
).filter(
     task.Task.id == task_id,
     (task.Task.user_id == user_id) |
     (project.Project.user_id == user_id)
).first()

    if existing_task is None:
     raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

    if task_data.name is not None:
        existing_task.name = task_data.name

    if task_data.status is not None:
        existing_task.status = task_data.status

    if "due_date" in task_data.model_fields_set:
        existing_task.due_date = task_data.due_date

    db.commit()
    db.refresh(existing_task)

    return existing_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    existing_task = db.query(task.Task).join(
     project.Project,
     task.Task.project_id == project.Project.id
).filter(
     task.Task.id == task_id,
     (task.Task.user_id == user_id) |
     (project.Project.user_id == user_id)
).first()
    
    if existing_task is None:
     raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

    db.delete(existing_task)
    db.commit()

    return {"message": "Task deleted successfully"}