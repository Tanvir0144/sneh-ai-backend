import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.db.base import Base

class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    PLUS = "plus"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
    is_active = Column(Boolean(), default=True)
    
    # --- THIS IS THE NEW ADDITION ---
    # Field to identify admin users
    is_superuser = Column(Boolean(), default=False, nullable=False)
    # --- END OF ADDITION ---
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())