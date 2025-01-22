from sqlalchemy.orm import Session
from app.models import Confirmation
from app.models.step import Step
from app.models.tag import Tag
from app.schemas import ConfirmationCreate, ConfirmationUpdate, ConfirmationResponse;
from fastapi import HTTPException
from typing import List


def create_confirmation(db: Session, request: ConfirmationCreate) -> ConfirmationResponse:
    if request.tagIds:
        tags = db.query(Tag).filter(Tag.id.in_(request.tagIds)).all()
        if len(tags) != len(request.tagIds):
            raise HTTPException(status_code=400, detail="One or more tags with the given IDs do not exist")
    
    db_request = Confirmation(
        full_name=request.full_name,
        email=request.email,
        issue_type=request.issue_type,
        user_id=request.user_id,
        tags=tags  
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    steps = [
        Step(description=step_description, confirmation_id=db_request.id)
        for step_description in request.steps
    ]
    db.add_all(steps)
    db.commit()
    db.refresh(db_request)

    response = ConfirmationResponse(
        id=db_request.id,
        full_name=db_request.full_name,
        email=db_request.email,
        issue_type=db_request.issue_type,
        steps=request.steps, 
        tagIds=request.tagIds,  
        user_id=db_request.user_id,
    )
    return response

def get_confirmations(db: Session, skip: int = 0, limit: int = 100) -> List[ConfirmationResponse]:
   confirmations = db.query(Confirmation).offset(skip).limit(limit).all()
   return [ConfirmationResponse.from_orm(req) for req in confirmations]


def get_confirmation_by_id(db: Session, request_id: int) -> ConfirmationResponse:
    confirmation = db.query(Confirmation).filter(Confirmation.id == request_id).first()
    if not confirmation:
        raise HTTPException(status_code=404, detail="confirmation not found")
    return [
       ConfirmationResponse(
            id=confirmation.id,
            full_name=confirmation.full_name,
            email=confirmation.email, 
            issue_type=confirmation.issue_type,
            tagNames=[tag.name for tag in confirmation.tags],
            steps=[step.description for step in confirmation.steps],
            user_id=confirmation.user_id  
        )
    ]

def get_confirmations_by_user(db: Session, user_id: int) -> List[ConfirmationResponse]:
    confirmations = db.query(Confirmation).filter(Confirmation.user_id == user_id).all()
    if not confirmations:
        raise HTTPException(status_code=404, detail="No confirmations found for the user")
    
    return [
        ConfirmationResponse(
            id=confirmation.id,
            full_name=confirmation.full_name,
            email=confirmation.email, 
            issue_type=confirmation.issue_type,
            tagNames=[tag.name for tag in confirmation.tags],
            steps=[step.description for step in confirmation.steps],
            user_id=confirmation.user_id  
        )
        for confirmation in confirmations
    ]

def update_confirmation(db: Session, request_id: int, request: ConfirmationUpdate) -> ConfirmationResponse:
    db_request = db.query(Confirmation).filter(Confirmation.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="confirmation not found")
    
    for var, value in request.dict(exclude_unset=True).items():
        setattr(db_request, var, value)
    db.commit()
    db.refresh(db_request)

    return ConfirmationResponse.from_orm(db_request)


def delete_confirmation(db: Session, request_id: int) -> ConfirmationResponse:
    db_request = db.query(Confirmation).filter(Confirmation.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="confirmation not found")
    
    db.delete(db_request)
    db.commit()
    return [
       ConfirmationResponse(
            id=db_request.id,
            full_name=db_request.full_name,
            email=db_request.email, 
            issue_type=db_request.issue_type,
            tagNames=[tag.name for tag in db_request.tags],
            steps=[step.description for step in db_request.steps],
            user_id=db_request.user_id  
        )
    ]