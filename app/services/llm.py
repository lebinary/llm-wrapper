from app.models.LLMAgent import LLMAgent
from app.models.llm_strategies import OpenAIStrategy
from functools import lru_cache
from app.logger import logger
from app.custom_pipelines import CustomGenerateChatPipeline

@lru_cache()
def get_llm_agent():
    openai_strategy = OpenAIStrategy(CustomGenerateChatPipeline)
    return LLMAgent(openai_strategy)
