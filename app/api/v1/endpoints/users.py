from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import models
from app.schemas.user import User
from app.api.v1 import deps

router = APIRouter()

@router.get("/me", response_model=User)
def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    """
    Get current user's profile information.
    """
    return current_user