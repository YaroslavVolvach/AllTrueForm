from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.enums import Role
from dotenv import load_dotenv
import os

load_dotenv()

def create_admin():
    db: Session = SessionLocal()

    existing_admin = db.query(User).filter(User.role == Role.admin).first()
    if existing_admin:
        print("Admin already exists")
        return

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_full_name = os.getenv("ADMIN_FULL_NAME", "Default Admin")  

    if not admin_email or not admin_password:
        print("Error: ADMIN_EMAIL or ADMIN_PASSWORD is not set in .env")
        return

    admin = User(
        email=admin_email,
        hashed_password=hash_password(admin_password),
        full_name=admin_full_name,  
        role=Role.admin
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print(f"Admin {admin.email} was created.")

if __name__ == "__main__":
    create_admin()