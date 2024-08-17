from fastapi import FastAPI, APIRouter, Depends, File, UploadFile, Body, HTTPException
from typing import List, Any
from app.services.conversation import (
    create_conversation,
    get_conversations,
    get_conversation_by_id
)
from app.models.LLMAgent import get_llm_agent
from app.logger import logger
from app.schemas import (
    ChatReturn,
    ConversationReturn,
    ConversationCreate
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
from sqlalchemy.orm import (Session)
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError, NoResultFound


router = APIRouter()

@router.post("/", response_model=ConversationReturn, status_code=HTTP_201_CREATED)
async def create_new_conversation(
    conversation: ConversationCreate = Body(...),
    db: Session = Depends(get_db)
) -> ConversationReturn:
    try:
        new_conversation = await create_conversation(conversation=conversation, db=db)
        return new_conversation
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while creating conversation")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    except Exception as e:
        logger.exception("Unknown error occurred while creating conversation")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error occurred")


@router.get("/", response_model=List[ConversationReturn], status_code=HTTP_200_OK)
async def list_conversations(db: Session = Depends(get_db)) -> List[ConversationReturn]:
    try:
        conversations = await get_conversations(db=db)
        return [ConversationReturn.from_orm(c) for c in conversations]
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while getting conversations")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    except Exception as e:
        logger.exception("Unknown error occurred while getting conversation")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error occurred")


@router.get("/{conversation_id}", response_model=List[ConversationReturn], status_code=HTTP_200_OK)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)) -> ConversationReturn:
    try:
        conversation = await get_conversation_by_id(conversation_id=conversation_id,db=db)
        return conversation
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

@router.post("/chat")
async def llm_chat(prompt: str, llm_agent=Depends(get_llm_agent)) -> ChatReturn:
    result = await llm_agent.chat(prompt)
    return ChatReturn(value=result)

def init_app(app: FastAPI):
    app.include_router(router, prefix="/conversations", tags=["conversations"])
