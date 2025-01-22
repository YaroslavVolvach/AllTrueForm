from pydantic import BaseModel, validator
from typing import List, Optional
from app.enums import IssueType
from app.models import Step

class ConfirmationCreate(BaseModel):
    full_name: str
    email: str
    issue_type: IssueType
    tagIds: List[int]  
    steps: List[str]
    user_id: int

    @validator('steps')
    def check_steps(cls, v):
        if not v:
            raise ValueError('At least one step is required.')
        return v

    class Config:
        orm_mode = True

class ConfirmationUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    issue_type: Optional[IssueType] = None
    tagIds: Optional[List[int]] = None
    steps: Optional[List[str]] = None


    class Config:
        orm_mode = True



class ConfirmationResponse(BaseModel):
    id: int
    full_name: str
    email: str
    issue_type: IssueType
    tagNames: Optional[List[str]] = None
    steps: List[str]  
    user_id: Optional[int]

    class Config:
        orm_mode = True


class ConfirmationDelete(BaseModel):
    confirmation_id: int
    token: str
