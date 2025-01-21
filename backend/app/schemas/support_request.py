from pydantic import BaseModel
from typing import List

class SupportRequestCreate(BaseModel):
    title: str
    description: str
    tags: List[str]

    class Config:
        orm_mode = True