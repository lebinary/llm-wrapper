from sqlalchemy.orm import class_mapper
import os
import re

def orm_to_dict(orm_object):
    return {
        column.key: getattr(orm_object, column.key)
        for column in class_mapper(orm_object.__class__).mapped_table.columns
    }

def filename_to_conversation_title(filename: str) -> str:
    name_without_extension = os.path.splitext(filename)[0]
    name_with_spaces = re.sub(r'[_-]', ' ', name_without_extension)
    title = name_with_spaces.title()
    title = title.strip()

    return title
