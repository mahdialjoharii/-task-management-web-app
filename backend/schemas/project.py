from pydantic import BaseModel, field_validator


class ProjectCreate(BaseModel):
    project_name: str

    @field_validator("project_name")
    @classmethod
    def validate_project_name(cls, value):
        if not value.strip():
            raise ValueError("Project name cannot be empty")
        return value


class ProjectResponse(BaseModel):
    id: int
    project_name: str
    user_id: int