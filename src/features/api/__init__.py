from fastapi import FastAPI

from src.features.api.api_route import create_router
from src.features.api.store_bottle import register_feature as register_store_bottle


def register_feature(app: FastAPI) -> None:
    app.include_router(create_router())
    register_store_bottle(app)

