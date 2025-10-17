from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import models
from app.schemas.chat import ChatRequest, ChatResponse
from app.api.v1 import deps
from app.services import chat_service
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def handle_chat(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
    chat_request: ChatRequest,
):
    """
    Handle an incoming chat message from a user.
    """
    # Find conversation or create a new one
    conversation_id = chat_request.conversation_id
    if conversation_id:
        conversation = db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == current_user.id
        ).first()
        if not conversation:
            # Create a new conversation if ID is invalid or doesn't belong to the user
            conversation = models.Conversation(user_id=current_user.id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
    else:
        conversation = models.Conversation(user_id=current_user.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    user_message = models.ConversationMessage(
        conversation_id=conversation.id,
        role="user",
        content=chat_request.message
    )
    db.add(user_message)

    # Get AI response from the service
    ai_reply_text = chat_service.get_ai_response(message=chat_request.message)

    # Save AI response
    ai_message = models.ConversationMessage(
        conversation_id=conversation.id,
        role="ai",
        content=ai_reply_text
    )
    db.add(ai_message)
    
    # Commit all changes to the database
    db.commit()

    return ChatResponse(reply=ai_reply_text, conversation_id=conversation.id)