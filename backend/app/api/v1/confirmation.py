from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud
from app.schemas import ConfirmationCreate, ConfirmationDelete, ConfirmationResponse, UserRequest;
from app.db import get_db
from app.enums import Role
from app.dependencies import role_required
from typing import List

router = APIRouter()

@router.post("/", response_model=ConfirmationResponse)
def create_confirmation(
    request: ConfirmationCreate,
    db: Session = Depends(get_db),
): 
    return crud.create_confirmation(db=db, request=request)


@router.get("/", response_model=List[ConfirmationResponse])
def get_all_confirmations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_role: str = Depends(role_required(Role.admin))  
):
    return crud.get_confirmation(db=db, skip=skip, limit=limit)


@router.post("/my-confirmations", response_model=List[ConfirmationResponse])
def get_confirmation_by_user_id(
    body: UserRequest, 
    db: Session = Depends(get_db),
):
    current_user = crud.get_current_user(db, body.token)
    if current_user.id != body.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.get_confirmations_by_user(db=db, user_id=body.user_id)

@router.delete("/confirmation_delete", response_model=ConfirmationResponse)
def delete_confirmation(
    body: ConfirmationDelete,
    db: Session = Depends(get_db),
):
    current_user = crud.get_current_user(db, body.token)
    confirmation = crud.get_confirmation_by_id(db=db, request_id=body.confirmation_id)
    if confirmation.user_id != current_user.id and current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.delete_confirmation(db=db, request_id=body.confirmation_id)


'''''
@router.get("/{confirmation_id}", response_model=ConfirmationResponse) 
def get_confirmation_by_id(
    confirmation_id: int,
    token:str,
    db: Session = Depends(get_db),
):
    current_user = crud.get_current_user(db, token)
    confirmation = crud.get_confirmation_by_id(db=db, request_id=confirmation_id)
    if confirmation.user_id != current_user.id and current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return confirmation


@router.put("/{confirmation_id}", response_model=ConfirmationResponse)
def update_confirmation(
    confirmation_id: int,
    request: ConfirmationUpdate,
    token:str,
    db: Session = Depends(get_db),
):
    current_user = crud.get_current_user(db, token)
    confirmation = crud.get_confirmation_by_id(db=db, request_id=confirmation_id)
    if confirmation.user_id != current_user.id and current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.update_confirmation(db=db, request_id=confirmation_id, request=request)

'''''

