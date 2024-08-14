from .llm_strategies import LLMStrategy
from typing import List, Dict

class LLM:
    def __init__(self, strategy: LLMStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: LLMStrategy):
        self._strategy = strategy

    async def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        return await self._strategy.generate_text(prompt, max_tokens)

    async def generate_chat(self, messages: List[Dict[str, str]], max_tokens: int = 100) -> str:
        return await self._strategy.generate_chat(messages, max_tokens)

    async def embed_text(self, text: str) -> List[float]:
        return await self._strategy.embed_text(text)
