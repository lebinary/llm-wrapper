from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
from pandasai import Agent
from pandasai.llm import OpenAI
import pandas as pd
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
    def __init__(self, pipeline: Optional[Type[GenerateChatPipeline]] = None):
        llm = OpenAI(api_token=os.environ.get("OPEN_API_KEY"))
        df = pd.DataFrame({
            "brand": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            "region": ["North America", "North America", "North America", "North America", "North America", "Europe", "Europe", "Europe", "Europe", "Europe"],
            "sales": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        })

        self.agent = Agent(
            df,
            pipeline=pipeline,
            config={
                "llm": llm,
                "verbose": True
            }
        )

    async def chat(self, prompt: str) -> Union[str, int, float, DataFrame]:
        response = self.agent.chat(prompt)
        return response
