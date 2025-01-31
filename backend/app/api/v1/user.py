from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.session import get_db
from app.core.security import create_access_token, verify_password, hash_password
from app.enums import Role
from app.dependencies import role_required
from app.models import User

router = APIRouter()

@router.post("/registration", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.UserResponse)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role.value})
    return schemas.UserResponse(id=db_user.id, full_name=db_user.full_name, email=db_user.email, role=db_user.role, access_token=access_token, token_type="Bearer")


@router.get("/me", response_model=schemas.UserResponse)
def get_user_me(token: str, db: Session = Depends(get_db)):
    return crud.get_current_user(db, token)


@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user_role: str = Depends(role_required(Role.admin))):
    return crud.get_users(db)


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int, 
    user: schemas.UserUpdate, 
    db: Session = Depends(get_db), 
    current_user_role: str = Depends(role_required(Role.admin))
):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}", response_model=schemas.UserResponse)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user_role: str = Depends(role_required(Role.admin))
):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)


@router.put("/me/change-password", response_model=schemas.UserResponse)
def change_password(
    token: str,
    password_data: schemas.ChangePassword, 
    db: Session = Depends(get_db)
):
    current_user = crud.get_current_user(db, token)
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    hashed_password = hash_password(password_data.new_password)

    updated_user = crud.update_user_password(db=db, user_id=current_user.id, new_password=hashed_password)
    
    return schemas.UserResponse.from_orm(updated_user)