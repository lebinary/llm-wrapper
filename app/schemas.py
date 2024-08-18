from typing import Union, Any, Optional, List
from pandas import DataFrame
from pydantic import BaseModel, Field, validator
import json
from datetime import datetime

class ChatReturn(BaseModel):
    value: Any

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "value": "The answer is yes",
            }
        }

    @validator('value')
    def serialize_dataframe(cls, v):
        if isinstance(v, DataFrame):
            return v.to_dict(orient='records')
        return v

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        if isinstance(d['value'], DataFrame):
            d['value'] = d['value'].to_dict(orient='records')
        return d

    def json(self, *args, **kwargs):
        return json.dumps(self.dict(*args, **kwargs))

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
