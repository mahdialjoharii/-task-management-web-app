from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from dependencies import get_db
from models import project, task
from schemas.project import ProjectCreate, ProjectResponse
from auth import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    projects = db.query(project.Project).filter(
     project.Project.user_id == user_id
).all()
    return projects


@router.post("/", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    
    new_project = project.Project(
        project_name=project_data.project_name,
        user_id=user_id
    )

    try:
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User does not exist"
        )

    return new_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    existing_project = db.query(project.Project).filter(
        project.Project.id == project_id,
        project.Project.user_id == user_id
    ).first()

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    existing_project.project_name = project_data.project_name
    

    try:
        db.commit()
        db.refresh(existing_project)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User does not exist"
        )

    return existing_project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    existing_project = db.query(project.Project).filter(
      project.Project.id == project_id,
      project.Project.user_id == user_id
).first()

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    db.query(task.Task).filter(
    task.Task.project_id == project_id
).delete()
    db.delete(existing_project)
    db.commit()

    return {"message": "Project deleted successfully"}