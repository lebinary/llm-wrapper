from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from app.logger import logger
from typing import List, Optional
import importlib
import os
import sys
from app.database import init_db, init_async_db
import asyncio

async def initialize_databases():
    await init_async_db()
    init_db()

def discover_modules(directory: str = 'app/routes') -> list[str]:
    module_names = []
    for file in os.listdir(directory):
        if file.endswith('.py') and not file.startswith('__'):
            module_names.append(file[:-3])
    return module_names

def load_modules(app: FastAPI) -> None:
    for module_name in discover_modules():
        try:
            module = importlib.import_module(f'app.routes.{module_name}')

            if hasattr(module, 'init_app') and callable(module.init_app):
                module.init_app(app)
                logger.info(f"Loaded Module: {module_name}.")
            else:
                logger.warning(f"Warning: Module {module_name} does not have an init_app function")
        except ImportError as e:
            logger.error(f"Error importing module {module_name}: {e}")

def app_init() -> FastAPI:
    logger.info("Initializing app")

    app = FastAPI(
        title="llm-wrapper",
        debug=False
    )

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.async_client = httpx.AsyncClient()

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting async client.")
        await initialize_databases()
        load_modules(app)

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Closing async client.")
        await app.state.async_client.aclose()

    return app
