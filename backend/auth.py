from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.revoked_token import RevokedToken

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "jti": str(uuid4())
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "require_exp": True,
                "require_jti": True
            }
        )

        user_id = payload.get("user_id")
        jti = payload.get("jti")

        if user_id is None or not jti:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        with SessionLocal() as db:
            revoked_token = db.query(RevokedToken).filter(
                RevokedToken.jti == jti
            ).first()

            if revoked_token is not None:
                raise HTTPException(
                    status_code=401,
                    detail="Token has been revoked"
                )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )