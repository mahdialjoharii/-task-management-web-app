from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database.database import Base, engine, SessionLocal
from models import user, project, task
from schemas.task import TaskCreate, TaskUpdate
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Task Management API is running"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks")
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
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

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(task.Task).all()
    return tasks

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    existing_task = db.query(task.Task).filter(
        task.Task.id == task_id
    ).first()

    if existing_task is None:
        return {"message": "Task not found"}

    if task_data.name is not None:
        existing_task.name = task_data.name

    if task_data.status is not None:
        existing_task.status = task_data.status

    if task_data.due_date is not None:
        existing_task.due_date = task_data.due_date

    db.commit()
    db.refresh(existing_task)

    return existing_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    existing_task = db.query(task.Task).filter(
        task.Task.id == task_id
    ).first()

    if existing_task is None:
        return {"message": "Task not found"}

    db.delete(existing_task)
    db.commit()

    return {"message": "Task deleted successfully"}