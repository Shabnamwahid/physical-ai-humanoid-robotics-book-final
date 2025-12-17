from fastapi import APIRouter, HTTPException, Depends
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import ChatRequest
from app.models.response import ChatResponse, ErrorResponse
from app.services.chat_service import ChatService
from app.services.db import get_db_session

logger = logging.getLogger(__name__)
router = APIRouter()
chat_service = ChatService()

@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        200: {"description": "Successful response"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def chat_endpoint(chat_request: ChatRequest, db: AsyncSession = Depends(get_db_session)):
    try:
        if not chat_request.message or not chat_request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Pass DB session to ChatService
        result = await chat_service.chat(
            query=chat_request.message,
            conversation_id=chat_request.conversation_id,
            top_k=chat_request.top_k or 5,
            max_tokens=chat_request.max_tokens,
            temperature=chat_request.temperature,
            context_window=chat_request.context_window or 3,
            db=db  # <- DB session added
        )

        response = ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            timestamp=result["timestamp"],
            sources=result.get("sources"),
            confidence=result.get("confidence")
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/chat/health")
async def chat_health():
    try:
        test_result = await chat_service.chat("test", top_k=1)
        return {"status": "healthy", "service": "chat"}
    except Exception as e:
        logger.error(f"Chat health check failed: {e}")
        raise HTTPException(status_code=500, detail="Chat service not healthy")
