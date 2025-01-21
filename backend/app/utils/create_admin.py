from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.enums import Role

def create_admin():
    db: Session = SessionLocal()

    existing_admin = db.query(User).filter(User.role == Role.admin).first()
    if existing_admin:
        print("Admin already exists")
        return

    admin = User(
        email="admin@example.com", 
        hashed_password=hash_password("adminpassword"),
        role=Role.admin
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print(f"Admin {admin.email} was created.")

if __name__ == "__main__":
    create_admin()