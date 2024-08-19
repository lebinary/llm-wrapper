from abc import ABC, abstractmethod
from typing import List, Any, Dict
import os
from fastapi import File
from app.logger import logger
import pandas as pd
from pandasai.llm import OpenAI
from app.db_models import File
from app.schemas import FileUpdate
from app.services.file import async_update_file
from builtins import ValueError
import re


class LLMStrategy(ABC):
    @property
    @abstractmethod
    def llm(self) -> Any:
        pass

    @abstractmethod
    def security_check(self, data: List[pd.DataFrame]) -> Any:
        pass

class OpenAIStrategy(LLMStrategy):
    def __init__(self):
        self._llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))

    @property
    def llm(self) -> OpenAI:
        return self._llm

    def security_check(self, data: List[pd.DataFrame]) -> List[pd.DataFrame]:
        secure_dfs = []

        for df in data:
            # Remove potentially sensitive columns
            sensitive_columns = ['password', 'ssn', 'credit_card', 'secret']
            df = df.drop(columns=[col for col in sensitive_columns if col in df.columns])

            # Redact email addresses and phone numbers
            for col in df.select_dtypes(include=['object']):
                df[col] = df[col].apply(self._redact_sensitive_info)

            # Limit the number of rows
            max_rows = 1000
            if len(df) > max_rows:
                df = df.sample(n=max_rows, random_state=42)

            # Ensure numerical values are within a reasonable range
            for col in df.select_dtypes(include=['int64', 'float64']):
                lower_bound, upper_bound = df[col].quantile([0.01, 0.99])
                df[col] = df[col].clip(lower_bound, upper_bound)

            secure_dfs.append(df)

        return secure_dfs

    def _redact_sensitive_info(self, text):
        if not isinstance(text, str):
            return text

        # Redact email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = re.sub(email_pattern, '[EMAIL REDACTED]', text)

        # Redact phone numbers (assumes a simple pattern, may need to be adjusted)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        text = re.sub(phone_pattern, '[PHONE REDACTED]', text)

        return text
