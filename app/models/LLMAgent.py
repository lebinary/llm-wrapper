from app.llm_strategies import LLMStrategy
from typing import List, Dict, Any
from app.custom_pipelines import CustomGenerateChatPipeline
from app.llm_strategies import OpenAIStrategy
from typing import Optional, Type
from pandasai.pipelines.chat.generate_chat_pipeline import GenerateChatPipeline
from pandasai import Agent
import pandas as pd
import os

class LLMAgent:
    def __init__(
        self,
        file_paths: List[str],
        strategy: LLMStrategy=OpenAIStrategy(),
        pipeline: Optional[Type[GenerateChatPipeline]] = None
    ):
        self._strategy = strategy
        self._pipeline = pipeline
        self._file_paths = file_paths
        self._data = None
        self._agent = None

    @classmethod
    async def create(
        cls,
        file_paths: List[str],
        strategy: LLMStrategy = OpenAIStrategy(),
        pipeline: Optional[Type[GenerateChatPipeline]] = None
    ):
        instance = cls(file_paths, strategy, pipeline)
        await instance._initialize()
        return instance

    async def _initialize(self):
        self._data = await self._strategy.preprocess_data(self._file_paths)

        if self._data.empty:
            raise ValueError("No data has been loaded. Please provide valid file paths.")

        self._update_agent()

    async def set_strategy(self, strategy: LLMStrategy):
        self._strategy = strategy
        self._data = await self._strategy.preprocess_data(self._file_paths)
        self._update_agent()

    def _update_agent(self):
        if self._data is None:
            raise ValueError("No data has been loaded. Please update the data first.")

        self._agent = Agent(
            self._data,
            pipeline=self._pipeline,
            config={
                "llm": self._strategy.llm,
                "verbose": True
            }
        )

    async def chat(self, prompt: str) -> Any:
        if self._data is None:
            raise ValueError("No data has been loaded. Please update the data first.")
        if self._agent is None:
            raise ValueError("No agent has been created. Please create the agent first.")

        return self._agent.chat(prompt)
