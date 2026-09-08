from datetime import date
from pydantic import BaseModel
from enum import Enum


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TaskCreate(BaseModel):
    name: str
    project_id: int
    assigned_user_id: int
    status: TaskStatus = TaskStatus.TODO
    due_date: date | None = None


class TaskUpdate(BaseModel):
    name: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None 

class TaskResponse(BaseModel):
    id: int
    name: str
    project_id: int
    user_id: int
    status: str
    due_date: date | None = None       