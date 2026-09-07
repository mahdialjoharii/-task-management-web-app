from pydantic import BaseModel


class ProjectCreate(BaseModel):
    project_name: str
    user_id: int


class ProjectResponse(BaseModel):
    id: int
    project_name: str
    user_id: int