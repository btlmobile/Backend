from fastapi import FastAPI

from src.features.sea.bottle import register_feature as register_bottle


def register_feature(app: FastAPI) -> None:
    register_bottle(app)


__all__ = ["register_feature"]

