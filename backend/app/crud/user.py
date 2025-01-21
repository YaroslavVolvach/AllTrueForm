from sqlalchemy.orm import Session
from app.models.user import User
from app import schemas
from app.core.security import hash_password, verify_token
from app.enums import Role
from fastapi import HTTPException


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(email=user.email, hashed_password=hash_password(user.password), role=Role.user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.hashed_password = hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def update_user_password(db: Session, user_id: int, hashed_password: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.hashed_password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user


def get_current_user(db: Session, token: str) -> schemas.User:
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return schemas.User.from_orm(user)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Could not validate credentials: {str(e)}")
    


