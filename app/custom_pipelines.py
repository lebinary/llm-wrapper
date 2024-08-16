import os
import re
from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from pandasai import SmartDataframe
from pandasai.pipelines.chat.generate_chat_pipeline import GenerateChatPipeline
from pandasai.pipelines.pipeline import Pipeline
from pandasai.pipelines.chat.prompt_generation import PromptGeneration
from typing import List, Optional, Union
from pandasai.pipelines.pipeline_context import PipelineContext
from pandasai.helpers.logger import Logger
from pandasai.agent.base_judge import BaseJudge
from pandasai.pipelines.chat.validate_pipeline_input import ValidatePipelineInput
from pandasai.pipelines.chat.cache_lookup import CacheLookup
from pandasai.pipelines.chat.code_generator import CodeGenerator
from pandasai.pipelines.chat.code_cleaning import CodeCleaning
from pandasai.pipelines.chat.cache_population import CachePopulation
from pandasai.pipelines.chat.cache_population import CachePopulation
from pandasai.prompts.generate_python_code import GeneratePythonCodePrompt
from pandasai.prompts.base import BasePrompt

from app.logger import logger

class CustomGeneratePythonCodePrompt(GeneratePythonCodePrompt):
    template_path: str = "custom_generate_python_code.tmpl"

    def __init__(self, **kwargs):
        """Initialize the prompt."""
        self.props = kwargs

        # find path to template file
        current_dir_path = Path(__file__).parent
        path_to_template = os.path.join(current_dir_path, "templates")
        env = Environment(loader=FileSystemLoader(path_to_template))
        self.prompt = env.get_template(self.template_path)

        self._resolved_prompt = None


class CustomGeneratePythonCodeWithSQLPrompt(CustomGeneratePythonCodePrompt):
    template_path = "custom_generate_python_code_with_sql.tmpl"

class CustomPromptGeneration(PromptGeneration):
    def get_chat_prompt(self, context: PipelineContext) -> Union[str, BasePrompt]:
        config = context.get("config", {})
        viz_lib = config.get("data_viz_library", "matplotlib")
        output_type = context.get("output_type")

        prompt_class = CustomGeneratePythonCodeWithSQLPrompt if config.get("direct_sql") else CustomGeneratePythonCodePrompt

        return (
            prompt_class(
                context=context,
                last_code_generated=context.get("last_code_generated"),
                viz_lib=viz_lib,
                output_type=output_type,
            )
        )

class CustomGenerateChatPipeline(GenerateChatPipeline):
    def __init__(
        self,
        *args,
        on_code_generation=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.code_generation_pipeline = Pipeline(
            context=self.context,
            logger=self._logger,
            query_exec_tracker=self.query_exec_tracker,
            steps=[
                ValidatePipelineInput(),
                CacheLookup(),
                CustomPromptGeneration(
                    skip_if=self.is_cached,
                    on_execution=None,
                ),
                CodeGenerator(
                    skip_if=self.is_cached,
                    on_execution=on_code_generation,
                ),
                CachePopulation(skip_if=self.is_cached),
                CodeCleaning(
                    skip_if=self.no_code,
                    on_failure=self.on_code_cleaning_failure,
                    on_retry=self.on_code_retry,
                )
            ],
        )
