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
    FileReturn,
    PromptUpdate,
    PromptReturn,
    FileUpdate
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
from app.db_models import Conversation
from sqlalchemy.future import select
from app.services.file import get_file_by_id, update_file

router = APIRouter()

@router.put("/{file_id}", response_model=FileReturn, status_code=HTTP_200_OK)
def update_existing_file(
    file_id: int,
    body: FileUpdate = Body(...),
    db: Session = Depends(get_db)
) -> FileReturn:
    try:
        file = get_file_by_id(file_id, db=db)
        updated_file = update_file(file, file_data=body, db=db)

        return FileReturn.from_orm(updated_file)
    except NoResultFound as e:
        logger.exception("Record not found while getting file")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Record not found")
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while updating file")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    except Exception as e:
        logger.exception("Error occurred while updating file")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while updating file")\

def init_app(app: FastAPI):
    app.include_router(router, prefix="/files", tags=["files"])
