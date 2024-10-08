from typing import Union, Any, Optional, List
from pandas import DataFrame
from pydantic import BaseModel, Field, validator
import json
from datetime import datetime


class ChatBody(BaseModel):
    prompt_chat: str


class RatingBody(BaseModel):
    rating: int


class __BaseFile(BaseModel):
    filename: str
    path: str
    active: bool
    data: Optional[dict] = None
    top_row: Optional[int] = None

class FileUpdate(BaseModel):
    filename: Optional[str] = None
    path: Optional[str] = None
    active: Optional[bool] = None
    data: Optional[dict] = None
    top_row: Optional[int] = None

class FileReturn(__BaseFile):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class _BasePrompt(BaseModel):
    content: str
    conversation_id: int
    response: Optional[dict] = None
    rating: Optional[int] = Field(None, ge=1, le=5)


class PromptReturn(_BasePrompt):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PromptCreate(_BasePrompt):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Whats the best sales?"
            }
        }


class PromptUpdate(BaseModel):
    content: Optional[str] = None
    response: Optional[dict] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)


class _BaseConversation(BaseModel):
    title: str


class ConversationReturn(_BaseConversation):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    prompts: Optional[List[PromptReturn]] = None
    files: Optional[List[FileReturn]] = None

    class Config:
        from_attributes = True

class ConversationCreate(_BaseConversation):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Anylyze sale data"
            }
        }
