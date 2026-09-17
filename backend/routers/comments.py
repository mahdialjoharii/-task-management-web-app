from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from models import comment, task, project
from schemas.comment import CommentCreate, CommentResponse
from auth import get_current_user


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post(
    "/",
    response_model=CommentResponse
)
def create_comment(
    comment_data: CommentCreate,
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

    new_comment = comment.Comment(
        content=comment_data.content,
        task_id=task_id,
        user_id=user_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.get(
    "/",
    response_model=list[CommentResponse]
)
def get_comments(
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

    comments = db.query(comment.Comment).filter(
        comment.Comment.task_id == task_id
    ).all()

    return comments

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    existing_comment = db.query(comment.Comment).join(
        task.Task,
        comment.Comment.task_id == task.Task.id
    ).join(
        project.Project,
        task.Task.project_id == project.Project.id
    ).filter(
        comment.Comment.id == comment_id,
        (comment.Comment.user_id == user_id) |
        (project.Project.user_id == user_id)
    ).first()

    if existing_comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    db.delete(existing_comment)
    db.commit()

    return {
        "message": "Comment deleted successfully"
    }

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    existing_comment = db.query(comment.Comment).join(
        task.Task,
        comment.Comment.task_id == task.Task.id
    ).join(
        project.Project,
        task.Task.project_id == project.Project.id
    ).filter(
        comment.Comment.id == comment_id,
        (comment.Comment.user_id == user_id) |
        (project.Project.user_id == user_id)
    ).first()

    if existing_comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    existing_comment.content = comment_data.content

    db.commit()
    db.refresh(existing_comment)

    return existing_comment