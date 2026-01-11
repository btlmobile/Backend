from fastapi import FastAPI
from src.features.chat.chat_route import chat_router


def register_feature(app: FastAPI) -> None:
    app.include_router(chat_router, prefix="/chat", tags=["Global Chat"])


__all__ = ["register_feature"]
