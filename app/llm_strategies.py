from abc import ABC, abstractmethod
from typing import List, Any, Dict
import os
from fastapi import File
from app.logger import logger
import pandas as pd
from pandasai.llm import OpenAI
from app.db_models import File

class LLMStrategy(ABC):
    @property
    @abstractmethod
    def llm(self) -> Any:
        pass

    @abstractmethod
    async def preprocess_data(self, files: List[File]) -> Any:
        pass

class OpenAIStrategy(LLMStrategy):
    def __init__(self):
        self._llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))

    @property
    def llm(self) -> OpenAI:
        return self._llm

    async def preprocess_data(self, files: List[File]) -> Dict[int, pd.DataFrame]:
        processed_data = {}
        for f in files:
            if f.path.endswith('.csv'):
                df = pd.read_csv(f.path)
            elif f.path.endswith('.xlsx') or f.path.endswith('.xls'):
                df = pd.read_excel(f.path)
            else:
                raise ValueError(f"Unsupported file format: {f.path}")

            processed_data[f.id] = df

        return processed_data
