from pydantic import BaseModel
from typing import Optional
from app.enums import Role


class UserCreate(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]


class User(BaseModel):
    id: int
    email: str
    role: Role

    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str