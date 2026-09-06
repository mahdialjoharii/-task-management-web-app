from datetime import date

from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str
    project_id: int
    user_id: int
    status: str = "TODO"
    due_date: date | None = None


class TaskUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    due_date: date | None = None    