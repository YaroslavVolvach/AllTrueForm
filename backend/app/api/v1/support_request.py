from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import support_request as crud_sr
from app.schemas import SupportRequestCreate, SupportRequestUpdate, SupportRequestResponse
from app.db import get_db
from app.dependencies import get_current_user, role_required
from app.enums import Role
from typing import List

router = APIRouter()

# Create
@router.post("/", response_model=SupportRequestResponse)
def create_support_request(
    request: SupportRequestCreate,
    db: Session = Depends(get_db),
    current_user_role: str = Depends(role_required(Role.user))
): 
   
    return crud_sr.create_support_request(db=db, request=request)


# Read all (for admins only)
@router.get("/", response_model=List[SupportRequestResponse])
def get_all_support_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_role: str = Depends(role_required(Role.admin))  
):
    
    return crud_sr.get_support_requests(db=db, skip=skip, limit=limit)


# Read by ID (for owner or admin)
@router.get("/{support_request_id}", response_model=SupportRequestResponse)
def get_support_request_by_id(
    support_request_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
   
    support_request = crud_sr.get_support_request_by_id(db=db, request_id=support_request_id)
    if not support_request:
        raise HTTPException(status_code=404, detail="Support Request not found")
    
    if current_user.role != Role.admin and support_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return support_request


# Read by User ID (admin or same user)
@router.get("/user/{user_id}", response_model=List[SupportRequestResponse])
def get_support_requests_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    if current_user.role != Role.admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return crud_sr.get_support_requests_by_user_id(db=db, user_id=user_id)


# Update (for admin or owner)
@router.put("/{support_request_id}", response_model=SupportRequestResponse)
def update_support_request(
    support_request_id: int,
    request: SupportRequestUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
   
    support_request = crud_sr.get_support_request_by_id(db=db, request_id=support_request_id)
    if not support_request:
        raise HTTPException(status_code=404, detail="Support Request not found")
    
    if current_user.role != Role.admin and support_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud_sr.update_support_request(db=db, request_id=support_request_id, request=request)


@router.delete("/{support_request_id}", response_model=SupportRequestResponse)
def delete_support_request(
    support_request_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    support_request = crud_sr.get_support_request_by_id(db=db, request_id=support_request_id)
    if not support_request:
        raise HTTPException(status_code=404, detail="Support Request not found")
    
    if current_user.role != Role.admin and support_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud_sr.delete_support_request(db=db, request_id=support_request_id)