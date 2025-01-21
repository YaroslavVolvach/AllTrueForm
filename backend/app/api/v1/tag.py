from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import tag as crud_tag
from app.schemas import TagCreate, Tag
from app.db import get_db

router = APIRouter()

@router.post("/", response_model=Tag)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = crud_tag.get_tag_by_name(db, name=tag.name)
    if db_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")
    return crud_tag.create_tag(db=db, name=tag.name)

@router.get("/", response_model=list[Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_tag.get_tags(db=db, skip=skip, limit=limit)