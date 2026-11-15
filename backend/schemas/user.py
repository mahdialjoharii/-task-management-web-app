from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password cannot be empty or whitespace")

        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 bytes")

        return value

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
class UserPublicResponse(BaseModel):
    id: int
    username: str    