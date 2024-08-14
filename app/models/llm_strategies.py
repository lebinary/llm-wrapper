from abc import ABC, abstractmethod
from typing import List, Dict

class LLMStrategy(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        pass

    @abstractmethod
    async def generate_chat(self, messages: List[Dict[str, str]], max_tokens: int = 100) -> str:
        pass

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        pass


class OpenAIStrategy(LLMStrategy):
    def __init__(self, api_key: str):
        # Initialize OpenAI client here
        self.api_key = api_key

    async def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        # Implement OpenAI text generation
        return f"OpenAI generated text for: {prompt}"

    async def generate_chat(self, messages: List[Dict[str, str]], max_tokens: int = 100) -> str:
        # Implement OpenAI chat generation
        return f"OpenAI generated chat response for: {messages[-1]['content']}"

    async def embed_text(self, text: str) -> List[float]:
        # Implement OpenAI text embedding
        return [0.1, 0.2, 0.3]


class ClaudeStrategy(LLMStrategy):
    def __init__(self, api_key: str):
        # Initialize Claude client here
        self.api_key = api_key

    async def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        # Implement Claude text generation
        return f"Claude generated text for: {prompt}"

    async def generate_chat(self, messages: List[Dict[str, str]], max_tokens: int = 100) -> str:
        # Implement Claude chat generation
        return f"Claude generated chat response for: {messages[-1]['content']}"

    async def embed_text(self, text: str) -> List[float]:
        # Implement Claude text embedding
        return [0.4, 0.5, 0.6]
