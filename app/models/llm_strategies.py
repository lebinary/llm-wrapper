from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
from pandasai import Agent
from pandasai.llm import OpenAI
import pandas as pd
from fastapi import File
from app.logger import logger

class LLMStrategy(ABC):
    @abstractmethod
    async def chat(self, prompt: Any) -> str:
        pass

class OpenAIStrategy(LLMStrategy):
    def __init__(self, description: str):
        llm = OpenAI(api_token=os.environ.get("OPEN_API_KEY"))
        self.agent = Agent([], description=description, config={"llm": llm, "verbose": True})

    async def chat(self, prompt: str) -> str:
        response = self.agent.chat(prompt)
        logger.info(f"RESPONSE: {response}")
        return response
