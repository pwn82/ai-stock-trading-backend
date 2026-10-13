from fastapi import APIRouter

from app.models.schemas import (
    ChatRequest
)

from app.services.chat_service import (
    chat_service
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


@router.post("")
def chat(
    request: ChatRequest
):

    response = chat_service.ask(
        question=request.question,
        stock_symbol=request.stock_symbol
    )

    return {
        "answer": response
    }