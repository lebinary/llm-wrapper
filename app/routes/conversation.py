from fastapi import FastAPI, APIRouter, Depends, File, UploadFile, Body, HTTPException, Query
from typing import List, Any, Optional
from app.utils import filename_to_conversation_title
from sqlalchemy.orm.strategy_options import selectinload
from app.services.conversation import (
    create_conversation,
    get_conversations,
    get_conversation_by_id,
    add_files_to_conversation,
    get_all_conversations
)
from app.services.agent import get_or_create_llm_agent
from app.logger import logger
from app.schemas import (
    ChatReturn,
    ConversationReturn,
    ConversationCreate,
    PromptCreate,
    PromptReturn,
    PromptUpdate
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_402_PAYMENT_REQUIRED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_423_LOCKED,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_408_REQUEST_TIMEOUT,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.database import get_db, get_async_db
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from app.utils import orm_to_dict
from app.db_models import Conversation
from sqlalchemy.future import select
from app.services.prompt import async_create_prompt, async_update_prompt

router = APIRouter()

@router.post("/", response_model=ConversationReturn, status_code=HTTP_201_CREATED)
def create_new_conversation(
    conversation: ConversationCreate = Body(...),
    db: Session = Depends(get_db)
) -> ConversationReturn:
    try:
        new_conversation = create_conversation(conversation=conversation, db=db)
        return ConversationReturn.from_orm(new_conversation)
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while creating conversation")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    except Exception as e:
        logger.exception("Unknown error occurred while creating conversation")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error occurred")


@router.get("/", response_model=List[ConversationReturn], status_code=HTTP_200_OK)
def list_conversations(db: Session = Depends(get_db)) -> List[ConversationReturn]:
    try:
        conversations = get_conversations(db=db)
        return [ConversationReturn.from_orm(c) for c in conversations]
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while getting conversations")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    except Exception as e:
        logger.exception("Unknown error occurred while getting conversation")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error occurred")


@router.get("/{conversation_id}", response_model=ConversationReturn, status_code=HTTP_200_OK)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)) -> ConversationReturn:
    try:
        conversation = get_conversation_by_id(conversation_id, db, with_prompts=True)
        return ConversationReturn(**orm_to_dict(conversation), prompts=[PromptReturn.from_orm(p) for p in conversation.prompts])
    except NoResultFound as e:
        logger.exception("Record not found while getting conversation")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Record not found")
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while getting conversation")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    except Exception as e:
        logger.exception("Unknown error occurred while getting conversation")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error occurred")


@router.post("/upload", response_model=ConversationReturn, status_code=HTTP_201_CREATED)
async def upload_files(
    conversation_id: Optional[int] = Query(None, description="Existing conversation ID. If not provided, a new conversation will be created."),
    title: Optional[str] = Query(None, description="Title for the new conversation if one is being created."),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
) -> ConversationReturn:
    try:
        # Create a new conversation if none provided
        updload_conversation_id = conversation_id
        if updload_conversation_id is None:
            new_conversation_title = title or (filename_to_conversation_title(files[0].filename) if files[0].filename else "New Conversation")
            new_conversation = create_conversation(ConversationCreate(title=new_conversation_title), db)
            updload_conversation_id = new_conversation.id

        updated_conversation = await add_files_to_conversation(updload_conversation_id, files, db)
        return ConversationReturn.from_orm(updated_conversation)
    except NoResultFound as e:
        logger.exception("Record not found while getting conversation")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Record not found")
    except Exception as e:
        logger.exception("Error occurred while uploading files")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while uploading files")

@router.post("/{conversation_id}/chat", response_model=ChatReturn, status_code=HTTP_200_OK)
async def llm_chat(
    conversation_id: int,
    prompt_chat: str,
    db: AsyncSession = Depends(get_async_db)
) -> ChatReturn:
    try:
        new_prompt = await async_create_prompt(PromptCreate(content=prompt_chat, conversation_id=conversation_id, rating=None), db)

        llm_agent = await get_or_create_llm_agent(conversation_id, db)
        llm_response = await llm_agent.chat(prompt_chat)

        str_llm_response = str(llm_response)
        updated_prompt = await async_update_prompt(new_prompt, prompt_data=PromptUpdate(response=str_llm_response), db=db)

        return ChatReturn(value=str_llm_response)
    except NoResultFound as e:
        logger.exception("Record not found while getting conversation")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Record not found")
    except Exception as e:
        logger.exception("Error occurred while chatting with llm")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while chatting with llm")

def init_app(app: FastAPI):
    app.include_router(router, prefix="/conversations", tags=["conversations"])
