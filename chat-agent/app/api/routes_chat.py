import uuid
from fastapi import APIRouter, Depends, Request
from fastapi.concurrency import run_in_threadpool
from strands import Agent

from app.schemas import ChatRequest, ChatResponse
from app.utils import get_agent
from app.core import logger

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    payload: ChatRequest,
    request: Request,
    agent: Agent = Depends(get_agent),
) -> ChatResponse:
    request_id = str(uuid.uuid4())
    logger.info(
        "request_id=%s path=%s message=%r",
        request_id, request.url.path, payload.message
    )

    result = await run_in_threadpool(agent, payload.message)

    logger.info(
        "request_id=%s response=%r",
        request_id, str(result)
    )

    return ChatResponse(response=str(result))
