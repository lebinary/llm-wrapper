from app.models.LLMAgent import LLMAgent
from app.models.llm_strategies import OpenAIStrategy
from functools import lru_cache

@lru_cache()
def get_llm_agent():
    openai_strategy = OpenAIStrategy("This is the agent's description")
    return LLMAgent(openai_strategy)
