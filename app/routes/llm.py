from fastapi import FastAPI, APIRouter
from app.models.llm_strategies import OpenAIStrategy, ClaudeStrategy
from app.models.Llm import LLM

router = APIRouter()

@router.get("/openai")
async def openai_llm():
    openai_strategy = OpenAIStrategy(api_key="your_openai_api_key")
    llm = LLM(openai_strategy)

    response = await llm.generate_text("Hello, world!")

    return response

@router.get("/claude")
async def claude_llm():
    claude_strategy = ClaudeStrategy(api_key="your_openai_api_key")
    llm = LLM(claude_strategy)

    response = await llm.generate_text("Hello, world!")

    return response

def init_app(app: FastAPI):
    app.include_router(router, prefix="/llm", tags=["llm"])
