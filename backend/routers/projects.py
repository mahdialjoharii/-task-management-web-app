from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dependencies import get_db
from models import project
from schemas.project import ProjectCreate

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(project.Project).all()
    return projects


@router.post("/")
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = project.Project(
        project_name=project_data.project_name,
        user_id=project_data.user_id
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


@router.put("/{project_id}")
def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    existing_project = db.query(project.Project).filter(
        project.Project.id == project_id
    ).first()

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    existing_project.project_name = project_data.project_name
    existing_project.user_id = project_data.user_id

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
    db: Session = Depends(get_db)
):
    existing_project = db.query(project.Project).filter(
        project.Project.id == project_id
    ).first()

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(existing_project)
    db.commit()

    return {"message": "Project deleted successfully"}