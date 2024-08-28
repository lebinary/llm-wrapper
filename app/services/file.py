from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import FileUpdate
from app.db_models import File
from sqlalchemy.orm import Session
from app.utils import create_update_dict
from sqlalchemy import update, case
from sqlalchemy.future import select
from typing import List, Sequence, Dict
from builtins import ValueError
import os
from pathlib import Path
from fastapi import UploadFile


UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {'.xls', '.xlsx', '.csv'}

def valid_file(file: File) -> bool:
    return file.active and file.data is not None and "df" in file.data

async def async_get_file_by_id(file_id: int, db: AsyncSession) -> File:
    query = select(File).filter_by(id=file_id)
    result = await db.execute(query)

    return result.scalars().one()

async def async_update_file(file: File, file_data: FileUpdate, db: AsyncSession) -> File:
    update_data = create_update_dict(File, file_data)

    query = update(File).where(File.id == file.id).values(update_data).returning(File)
    result = await db.execute(query)
    updated_file = result.scalars().one()

    await db.commit()
    await db.refresh(updated_file)

    return updated_file

async def save_uploaded_file(file: UploadFile) -> str:
    if not file.filename:
        raise ValueError("Filename is required")

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type. Only {', '.join(ALLOWED_EXTENSIONS)} are allowed.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate a file path
    project_dir_path = Path(__file__).parent.parent.parent
    base_path = os.path.join(project_dir_path, UPLOAD_DIR)
    file_path = os.path.join(base_path, file.filename)

    # Save the file content
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return file_path
