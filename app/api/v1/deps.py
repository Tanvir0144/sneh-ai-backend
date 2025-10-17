from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core import security
from app.core.config import settings
from app.db import models
from app.db.session import get_db
from app.schemas.token import TokenData

# This tells FastAPI where to look for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    Decode JWT token to get the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# --- THIS IS THE NEW ADDITION ---
def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Checks if the current user is an active superuser.
    If not, it raises a 403 Forbidden error. This is our 'Admin Lock'.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
# --- END OF ADDITION ---