from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import user
from schemas.user import UserCreate, UserResponse
from auth import hash_password,verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    users = db.query(user.User).all()
    return users

@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = user.User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    return new_user


@router.post("/login")
def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(user.User).filter(
        user.User.username == login_data.username
    ).first()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        login_data.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token({
    "user_id": existing_user.id
})

    return {
    "access_token": access_token,
    "token_type": "bearer"
}


@router.get("/me")
def get_me(user_id: int = Depends(get_current_user)):
    return {
        "user_id": user_id
    }

@router.post("/logout")
def logout(user_id: int = Depends(get_current_user)):
    return {
        "message": "Logged out successfully"
    }