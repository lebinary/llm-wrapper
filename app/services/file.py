from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import FileUpdate
from app.db_models import File
from sqlalchemy.orm import Session
from app.utils import create_update_dict
from sqlalchemy import update, case
from sqlalchemy.future import select
from typing import List, Sequence
from builtins import ValueError

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
