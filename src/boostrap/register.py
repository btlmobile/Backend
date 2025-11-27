from fastapi import FastAPI

from src.features import register_all_features


def setup_routes(app: FastAPI) -> None:
    register_all_features(app)

