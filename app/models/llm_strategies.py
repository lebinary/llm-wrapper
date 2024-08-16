from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
from pandasai import Agent
from pandasai.llm import OpenAI
from fastapi import File
from app.logger import logger
from typing import Optional, Type, Union
from pandasai.pipelines.chat.generate_chat_pipeline import GenerateChatPipeline
from pandas import DataFrame

class LLMStrategy(ABC):
    @abstractmethod
    async def chat(self, prompt: str) -> Any:
        pass

class OpenAIStrategy(LLMStrategy):
    def __init__(self, df: DataFrame, pipeline: Optional[Type[GenerateChatPipeline]] = None):
        openai_llm = OpenAI(api_token=os.environ.get("OPEN_API_KEY"))

        self.agent = Agent(
            df,
            pipeline=pipeline,
            config={
                "llm": openai_llm,
                "verbose": True
            }
        )

    async def chat(self, prompt: str) -> Union[str, int, float, DataFrame]:
        response = self.agent.chat(prompt)
        return response
