from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="New Chat")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    role = Column(String, nullable=False)  # "user" or "ai"
    content = Column(Text, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")