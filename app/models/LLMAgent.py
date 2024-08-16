from .llm_strategies import LLMStrategy
from typing import List, Dict, Any
from functools import lru_cache
from pandas import DataFrame
from app.custom_pipelines import CustomGenerateChatPipeline
from app.models.llm_strategies import OpenAIStrategy

class LLMAgent:
    def __init__(self, strategy: LLMStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: LLMStrategy):
        self._strategy = strategy

    async def chat(self, prompt: str) -> str:
        return await self._strategy.chat(prompt)

@lru_cache()
def get_llm_agent():
    df = DataFrame({
        "brand": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        "region": ["North America", "North America", "North America", "North America", "North America", "Europe", "Europe", "Europe", "Europe", "Europe"],
        "sales": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    })
    openai_strategy = OpenAIStrategy(df, CustomGenerateChatPipeline)
    return LLMAgent(openai_strategy)
