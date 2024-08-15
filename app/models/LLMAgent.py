from .llm_strategies import LLMStrategy
from typing import List, Dict, Any

class LLMAgent:
    def __init__(self, strategy: LLMStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: LLMStrategy):
        self._strategy = strategy

    async def chat(self, prompt: str) -> str:
        return await self._strategy.chat(prompt)
