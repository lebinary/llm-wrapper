from app.llm_strategies import LLMStrategy
from typing import List, Dict, Any
from app.custom_pipelines import CustomGenerateChatPipeline
from app.llm_strategies import OpenAIStrategy
from typing import Optional, Type
from pandasai.pipelines.chat.generate_chat_pipeline import GenerateChatPipeline
from pandasai import Agent
import pandas as pd
import os
from app.db_models import Conversation

class LLMAgent:
    def __init__(
        self,
        conversation: Conversation,
        strategy: LLMStrategy=OpenAIStrategy(),
        pipeline: Optional[Type[GenerateChatPipeline]] = None
    ):
        self._strategy = strategy
        self._pipeline = pipeline
        self._data = [pd.DataFrame(file.data) for file in conversation.files if file.active]
        self._agent = None

    @classmethod
    def create(
        cls,
        conversation: Conversation,
        strategy: LLMStrategy = OpenAIStrategy(),
        pipeline: Optional[Type[GenerateChatPipeline]] = None
    ):
        instance = cls(conversation, strategy, pipeline)
        instance.init_or_update_agent()
        return instance

    def init_or_update_agent(self):
        self._data = self._strategy.security_check(self._data)
        self._agent = Agent(
            self._data,
            pipeline=self._pipeline,
            config={
                "llm": self._strategy.llm,
                "verbose": True
            }
        )

    async def set_strategy(self, strategy: LLMStrategy):
        self._strategy = strategy
        self.init_or_update_agent()

    async def chat(self, prompt: str) -> Any:
        if self._agent is None:
            raise ValueError("No agent has been created. Please create the agent first.")

        if not self._data:
            return "No data has been loaded. Please update/select the data first."

        return self._agent.chat(prompt)
