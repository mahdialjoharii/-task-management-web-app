from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from models import task, project, user
from schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):

    existing_project = db.query(project.Project).filter(
    project.Project.id == task_data.project_id
).first()

    if existing_project is None:
     raise HTTPException(
        status_code=400,
        detail="Project does not exist"
    )
    existing_user = db.query(user.User).filter(
    user.User.id == task_data.user_id
).first()

    if existing_user is None:
     raise HTTPException(
        status_code=400,
        detail="User does not exist"
    )
    new_task = task.Task(
        name=task_data.name,
        project_id=task_data.project_id,
        user_id=task_data.user_id,
        status=task_data.status,
        due_date=task_data.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(task.Task).all()
    return tasks


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    existing_task = db.query(task.Task).filter(
        task.Task.id == task_id
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

    if task_data.due_date is not None:
        existing_task.due_date = task_data.due_date

    db.commit()
    db.refresh(existing_task)

    return existing_task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    existing_task = db.query(task.Task).filter(
        task.Task.id == task_id
    ).first()

    if existing_task is None:
     raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

    db.delete(existing_task)
    db.commit()

    return {"message": "Task deleted successfully"}