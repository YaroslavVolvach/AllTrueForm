from sqlalchemy.orm import Session
from app.models.user import User
from app import schemas
from app.core.security import hash_password, verify_token
from fastapi import HTTPException


def get_user_by_email(db: Session, email: str) -> schemas.UserResponse:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse.from_orm(user)


def create_user(db: Session, user: schemas.UserCreate) -> schemas.UserResponse:
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.fullName,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.UserResponse.from_orm(db_user)


def get_users(db: Session) -> list[schemas.UserResponse]:
    users = db.query(User).all()
    return [schemas.UserResponse.from_orm(user) for user in users]


def get_user(db: Session, user_id: int) -> schemas.UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse.from_orm(user)


def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> schemas.UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            db_user.hashed_password = hash_password(value)
        else:
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return schemas.UserResponse.from_orm(db_user)


def delete_user(db: Session, user_id: int) -> schemas.UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return schemas.UserResponse.from_orm(db_user)


def update_user_password(db: Session, user_id: int, new_password: str) -> schemas.UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(db_user)
    return schemas.UserResponse.from_orm(db_user)


def get_current_user(db: Session, token: str) -> schemas.UserResponse:
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return schemas.UserResponse.from_orm(user)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Could not validate credentials: {str(e)}")