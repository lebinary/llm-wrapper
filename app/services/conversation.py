from app.logger import logger
from sqlalchemy.orm import Session
from app.db_models import Conversation
from typing import List
from app.schemas import CreateConversation

async def create_conversation(conversation: CreateConversation, db: Session) -> Conversation:
    conversation = Conversation(**conversation.dict())
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

async def get_conversation_by_id(conversation_id: int, db: Session) -> Conversation:
    return db.query(Conversation).filter_by(id=conversation_id).one()

async def get_conversations(db: Session) -> List[Conversation]:
    return db.query(Conversation).all()
