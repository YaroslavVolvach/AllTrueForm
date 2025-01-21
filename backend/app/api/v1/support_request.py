from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import support_request as crud_sr, tag as crud_tag
from app.schemas import SupportRequestCreate
from app.db import get_db

router = APIRouter()

@router.post("/")
def create_support_request(request: SupportRequestCreate, db: Session = Depends(get_db)):
    tags = []
    for tag_name in request.tags:
        tag = crud_tag.get_tag_by_name(db, name=tag_name)
        if not tag:
            tag = crud_tag.create_tag(db, name=tag_name)
        tags.append(tag)
    return crud_sr.create_support_request(db=db, request=request, tags=tags)