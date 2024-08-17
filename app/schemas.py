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
                "type": "string",
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
    response: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class PromptReturn(_BasePrompt):
    id: int
    conversation_id: int
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



class _BaseConversation(BaseModel):
    title: str

class ConversationReturn(_BaseConversation):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    prompts: List[PromptReturn] = []

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
