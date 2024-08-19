from sqlalchemy.orm import class_mapper
import os
import re
from typing import Type, Any, Dict
from pydantic import BaseModel
import pandas as pd
from starlette.datastructures import UploadFile
from app.db_models import File
from builtins import ValueError

def orm_to_dict(orm_object):
    return {
        column.key: getattr(orm_object, column.key)
        for column in class_mapper(orm_object.__class__).mapped_table.columns
    }

def create_update_dict(model, update_data):
    return {
        getattr(model, column.key): getattr(update_data, column.key)
        for column in model.__table__.columns
        if hasattr(update_data, column.key) and getattr(update_data, column.key) is not None
    }

def filename_to_conversation_title(filename: str) -> str:
    name_without_extension = os.path.splitext(filename)[0]
    name_with_spaces = re.sub(r'[_-]', ' ', name_without_extension)
    title = name_with_spaces.title()
    title = title.strip()

    return title

def file_to_df(file_path: str) -> pd.DataFrame:
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
