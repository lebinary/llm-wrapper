from typing import Union, Any
from pandas import DataFrame
from pydantic import BaseModel, Field, validator
import json

class ReturnResult(BaseModel):
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
