from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Header, Query, Request, Response, status
from fastapi.responses import JSONResponse

from src.features.chat.chat_schema import ChatCreateRequest, ChatResponse
from src.features.chat.chat_service import ChatService


chat_router = APIRouter()
_chat_service = ChatService()


@chat_router.get("/global", response_model=list[ChatResponse])
async def get_global_chat(
    request: Request,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[ChatResponse]:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        # Since middleware only protects /api, we must enforce here if we want private chat
        # Return empty list or 401? Test expects 401.
        # But wait, return type is list[ChatResponse], throwing JSONResponse might be issue if not handled as exception?
        # FastAPI handles returning Response object from route returning model.
        # But better to raise HTTPException to be cleaner.
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth_required")

    messages = _chat_service.get_messages(limit=limit, authorization=auth_header)
    return [ChatResponse(**msg) for msg in messages]


@chat_router.post("/global", status_code=status.HTTP_204_NO_CONTENT)
async def send_global_chat(
    request: Request,
    payload: ChatCreateRequest,
) -> Response:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
         return JSONResponse(status_code=401, content={"error": "auth_required"})

    chat, error = _chat_service.create_message(payload, auth_header)
    if error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if error == "auth_required":
            status_code = status.HTTP_401_UNAUTHORIZED
        elif error != "internal_error":
             status_code = status.HTTP_400_BAD_REQUEST
             
        return JSONResponse(status_code=status_code, content={"error": error})
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
