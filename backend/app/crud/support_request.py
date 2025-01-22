from sqlalchemy.orm import Session
from app.models.support_request import SupportRequest
from app.models.step import Step
from app.models.tag import Tag
from app.schemas.support_request import SupportRequestCreate
from fastapi import HTTPException

def create_support_request(db: Session, request: SupportRequestCreate):
    if request.tagId:
        tag = db.query(Tag).filter(Tag.id == request.tagId).first()
        if not tag:
            raise HTTPException(status_code=400, detail="Tag with the given ID does not exist")
    
    db_request = SupportRequest(
        full_name=request.fullName,
        email=request.email,
        issue_type=request.issueType,
        tag_id=request.tagId 
    )
    db.add(db_request)
    db.commit()  
    db.refresh(db_request)

    steps = [
        Step(description=step_description, support_request_id=db_request.id)
        for step_description in request.steps
    ]
    db.add_all(steps)
    db.commit()

    db.refresh(db_request)
    return db_request

def get_support_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SupportRequest).offset(skip).limit(limit).all()

def get_support_request_by_id(db: Session, request_id: int):
    return db.query(SupportRequest).filter(SupportRequest.id == request_id).first()

def update_support_request(db: Session, request_id: int, request):
    db_request = get_support_request_by_id(db, request_id)
    if db_request:
        for var, value in request.dict(exclude_unset=True).items():
            setattr(db_request, var, value)
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        return db_request
    return None

def delete_support_request(db: Session, request_id: int):
    db_request = get_support_request_by_id(db, request_id)
    if db_request:
        db.delete(db_request)
        db.commit()
        return db_request
    return None