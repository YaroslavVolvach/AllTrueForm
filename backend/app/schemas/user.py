from pydantic import BaseModel, EmailStr
from typing import Optional
from app.enums import Role


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: Role  

    access_token: Optional[str]
    token_type: Optional[str]

    class Config:
        orm_mode = True
      
class UserCreate(BaseModel):
    fullName: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    fullName: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRequest(BaseModel):
    token: str
    user_id: int