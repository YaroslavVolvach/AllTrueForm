from sqlalchemy.orm import Session
from app.models.support_request import SupportRequest
from app.schemas.support_request import SupportRequestCreate

def create_support_request(db: Session, request: SupportRequestCreate):
    db_request = SupportRequest(**request.dict())
    db.add(db_request)
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