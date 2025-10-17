import datetime
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.sql import func
from app.db.base import Base

class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    chat_count = Column(Integer, default=0, nullable=False)
    image_count = Column(Integer, default=0, nullable=False)
    
    last_reset_date = Column(Date, default=func.current_date(), nullable=False)