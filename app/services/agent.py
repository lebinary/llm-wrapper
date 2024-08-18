from functools import lru_cache
from app.models.LLMAgent import LLMAgent
from app.llm_strategies import OpenAIStrategy
from app.custom_pipelines import CustomGenerateChatPipeline
from app.services.conversation import get_conversation_by_id, get_all_conversations, get_conversation_with_files
from sqlalchemy.orm import Session, joinedload, selectinload
from app.db_models import Conversation
from cachetools import TTLCache
from threading import Lock
from typing import List
from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession


llm_agent_cache = TTLCache(maxsize=100, ttl=3600)
cache_lock = Lock()

async def get_or_create_llm_agent(conversation_id: int, db: AsyncSession) -> LLMAgent:
    with cache_lock:
        if conversation_id not in llm_agent_cache:
            conversation = await get_conversation_with_files(conversation_id, db)

            file_paths: List[str] = [file.path for file in conversation.files]
            llm_agent = await LLMAgent.create(
                file_paths,
                strategy=OpenAIStrategy(),
                pipeline=CustomGenerateChatPipeline
            )
            llm_agent_cache[conversation_id] = llm_agent

    return llm_agent_cache[conversation_id]
