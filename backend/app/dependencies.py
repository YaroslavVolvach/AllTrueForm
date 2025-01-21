from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import get_role_from_token
from app.enums import Role
from app.db.session import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def role_required(role: Role):
    def wrapper(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        user_role = get_role_from_token(token)
        if user_role != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user_role
    return wrapper