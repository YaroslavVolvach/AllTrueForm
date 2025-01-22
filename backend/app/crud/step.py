from sqlalchemy.orm import Session
from app.models import Confirmation

def create_step(db: Session, confirmation_id: int, step: str):
    db_step = Confirmation(id=confirmation_id, steps=[step])
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step

def get_step_by_id(db: Session, step_id: int):
    return db.query(Confirmation).filter(Confirmation.id == step_id).first()

def get_steps_by_confirmation(db: Session, confirmation_id: int, skip: int = 0, limit: int = 100):
    return db.query(Confirmation).filter(Confirmation.id == confirmation_id).offset(skip).limit(limit).all()