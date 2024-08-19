from pandas.io.parsers.c_parser_wrapper import Sequence
from sqlalchemy.sql.sqltypes import Boolean
from app.logger import logger
from sqlalchemy.orm import Session, joinedload
from app.db_models import Conversation, File
from typing import List
from app.schemas import ConversationCreate
import os
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import selectinload
from builtins import ValueError
from app.utils import file_to_df
from fastapi import UploadFile
from app.services.file import save_uploaded_file


def create_conversation(conversation: ConversationCreate, db: Session) -> Conversation:
    new_conversation = Conversation(**conversation.dict())
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation


def get_conversation_by_id(
    conversation_id: int,
    db: Session,
    with_prompts: bool = False,
    with_files: bool = False
) -> Conversation:
    query = db.query(Conversation)

    if with_prompts:
        query = query.options(joinedload(Conversation.prompts))

    if with_files:
        query = query.options(joinedload(Conversation.files))

    return query.filter_by(id=conversation_id).one()


def get_conversations(db: Session) -> List[Conversation]:
    return db.query(Conversation).all()

async def get_conversation_with_files(conversation_id: int, db: AsyncSession) -> Conversation:
    query = select(Conversation).options(selectinload(Conversation.files)).filter_by(id=conversation_id)
    result = await db.execute(query)
    return result.scalars().one()

async def get_all_conversations(db: AsyncSession) -> Sequence[Conversation]:
    query = select(Conversation)
    result = await db.execute(query)
    conversations = result.scalars().all()
    return conversations

async def add_files_to_conversation(conversation_id: int, files: List[UploadFile], db: Session) -> Conversation:
    conversation = get_conversation_by_id(conversation_id, db)

    for file in files:
        # Save file to filesystem
        file_path = await save_uploaded_file(file)


        # Save file path to db
        df = file_to_df(file_path)
        db_file = File(filename=file.filename, path=file_path, conversation_id=conversation_id, data={"data": df.to_dict(orient='records')})
        db.add(db_file)

    db.commit()
    db.refresh(conversation)
    return conversation
