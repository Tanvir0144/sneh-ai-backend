from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.schemas.user import User as UserSchema # Rename to avoid conflict
from app.api.v1 import deps
from app.db.session import get_db

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def get_all_users(
    db: Session = Depends(get_db),
    # This endpoint is protected by our superuser dependency
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Get a list of all users in the system. (Admins only)
    """
    users = db.query(models.User).order_by(models.User.id).all()
    return users

@router.post("/ban/{user_id}", response_model=UserSchema)
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    # This endpoint is also protected
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Ban a user by setting their is_active status to False. (Admins only)
    """
    user_to_ban = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_ban:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_to_ban.is_active = False
    db.add(user_to_ban)
    db.commit()
    db.refresh(user_to_ban)
    return user_to_ban