from sqlalchemy.orm import Session
from app.models import SupportRequest

def create_step(db: Session, support_request_id: int, step: str):
    db_step = SupportRequest(id=support_request_id, steps=[step])  # Привязываем шаг к запросу
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step

def get_step_by_id(db: Session, step_id: int):
    return db.query(SupportRequest).filter(SupportRequest.id == step_id).first()

def get_steps_by_support_request(db: Session, support_request_id: int, skip: int = 0, limit: int = 100):
    return db.query(SupportRequest).filter(SupportRequest.id == support_request_id).offset(skip).limit(limit).all()