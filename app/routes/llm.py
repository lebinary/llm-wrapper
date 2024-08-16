from fastapi import FastAPI, APIRouter, Depends, File, UploadFile
from typing import List, Any
from app.services.llm import get_llm_agent
from app.logger import logger
from app.schemas import ReturnResult

router = APIRouter()

@router.post("/chat")
async def llm_chat(prompt: str, llm_agent=Depends(get_llm_agent)) -> ReturnResult:
    result = await llm_agent.chat(prompt)
    return ReturnResult(value=result)

def init_app(app: FastAPI):
    app.include_router(router, prefix="/llm", tags=["llm"])
