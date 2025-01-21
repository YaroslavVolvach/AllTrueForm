from app.models.user import User
from app.schemas.user import UserCreate
from app.db.session import SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, full_name=user.full_name, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user