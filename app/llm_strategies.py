from abc import ABC, abstractmethod
from typing import List, Any
import os
from fastapi import File
from app.logger import logger
import pandas as pd
from pandasai.llm import OpenAI

class LLMStrategy(ABC):
    @property
    @abstractmethod
    def llm(self) -> Any:
        pass

    @abstractmethod
    async def preprocess_data(self, file_paths: List[str]) -> Any:
        pass

class OpenAIStrategy(LLMStrategy):
    def __init__(self):
        self._llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))

    @property
    def llm(self) -> OpenAI:
        return self._llm

    async def preprocess_data(self, file_paths: List[str]) -> pd.DataFrame:
        dfs = []
        for file_path in file_paths:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            dfs.append(df)

        return pd.DataFrame() if not dfs else pd.concat(dfs, ignore_index=True)
