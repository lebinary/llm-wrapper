from app.llm_strategies import LLMStrategy
from typing import List, Dict, Any
from app.custom_pipelines import CustomGenerateChatPipeline
from app.llm_strategies import OpenAIStrategy
from typing import Optional, Type
from pandasai.pipelines.chat.generate_chat_pipeline import GenerateChatPipeline
from pandasai import Agent
import pandas as pd
import os
from app.db_models import File

class LLMAgent:
    def __init__(
        self,
        files: List[File],
        strategy: LLMStrategy=OpenAIStrategy(),
        pipeline: Optional[Type[GenerateChatPipeline]] = None
    ):
        self._strategy = strategy
        self._pipeline = pipeline
        self._files = files
        self._data: Optional[Dict[int, pd.DataFrame]] = None
        self._agent = None

    @classmethod
    async def create(
        cls,
        file_paths: List[File],
        strategy: LLMStrategy = OpenAIStrategy(),
        pipeline: Optional[Type[GenerateChatPipeline]] = None
    ):
        instance = cls(file_paths, strategy, pipeline)
        await instance._initialize()
        return instance

    async def _initialize(self):
        self._data = await self._strategy.preprocess_data(self._files)

        if not self._data:
            raise ValueError("No data has been loaded. Please provide valid files.")

        self.update_agent()

    def update_agent(self):
        if not self._data:
            raise ValueError("No data has been loaded. Please update the data first.")

        active_data = pd.concat([self._data[f.id] for f in self._files if f.active], ignore_index=True)

        self._agent = Agent(
            active_data,
            pipeline=self._pipeline,
            config={
                "llm": self._strategy.llm,
                "verbose": True
            }
        )

    async def set_strategy(self, strategy: LLMStrategy):
        self._strategy = strategy
        self._data = await self._strategy.preprocess_data(self._files)

        if not self._data:
            raise ValueError("No data has been loaded. Please provide valid files.")
        self.update_agent()

    async def chat(self, prompt: str) -> Any:
        if self._data is None:
            raise ValueError("No data has been loaded. Please update the data first.")
        if self._agent is None:
            raise ValueError("No agent has been created. Please create the agent first.")

        return self._agent.chat(prompt)
