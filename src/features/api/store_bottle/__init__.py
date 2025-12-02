from fastapi import FastAPI

from src.features.api.store_bottle.store_bottle_route import create_router


def register_feature(app: FastAPI) -> None:
    app.include_router(create_router())

