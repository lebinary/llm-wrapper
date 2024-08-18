from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import PromptCreate, PromptUpdate
from app.db_models import Prompt
from sqlalchemy.orm import Session
from app.utils import create_update_dict
from sqlalchemy import update

def get_prompt_by_id(prompt_id: int, db: Session) -> Prompt:
    query = db.query(Prompt)

    return query.filter_by(id=prompt_id).one()

def update_prompt(prompt: Prompt, prompt_data: PromptUpdate, db: Session) -> Prompt:
    update_data = create_update_dict(Prompt, prompt_data)

    db.query(Prompt).filter(Prompt.id == prompt.id).update(update_data)
    db.commit()
    db.refresh(prompt)

    return prompt

async def async_update_prompt(prompt: Prompt, prompt_data: PromptUpdate, db: AsyncSession) -> Prompt:
    update_data = create_update_dict(Prompt, prompt_data)

    query = update(Prompt).where(Prompt.id == prompt.id).values(update_data).returning(Prompt)
    result = await db.execute(query)
    updated_prompt = result.scalars().one()

    await db.commit()
    await db.refresh(updated_prompt)

    return updated_prompt

async def async_create_prompt(prompt: PromptCreate, db: AsyncSession) -> Prompt:
    new_prompt = Prompt(**prompt.dict())
    db.add(new_prompt)
    await db.commit()
    await db.refresh(new_prompt)

    return new_prompt
