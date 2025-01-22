from pydantic import BaseModel, validator
from typing import List
from app.enums import IssueType

class SupportRequestCreate(BaseModel):
    fullName: str
    email: str
    issueType: IssueType
    tagId: int  
    steps: List[str]

    @validator('steps')
    def check_steps(cls, v):
        if not v:
            raise ValueError('At least one step is required.')
        return v

    class Config:
        orm_mode = True