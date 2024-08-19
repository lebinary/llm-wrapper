from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import FileUpdate
from app.db_models import File
from sqlalchemy.orm import Session
from app.utils import create_update_dict
from sqlalchemy import update

def get_file_by_id(file_id: int, db: Session) -> File:
    query = db.query(File)

    return query.filter_by(id=file_id).one()

def update_file(file: File, file_data: FileUpdate, db: Session) -> File:
    update_data = create_update_dict(File, file_data)

    db.query(File).filter(File.id == file.id).update(update_data)
    db.commit()
    db.refresh(file)

    return file
