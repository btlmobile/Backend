from fastapi import FastAPI

from src.features.api import register_feature as register_api
from src.features.auth import register_feature as register_auth
from src.features.chat import register_feature as register_chat
from src.features.health import register_feature as register_health
from src.features.report import register_feature as register_report
from src.features.sea import register_feature as register_sea


def register_all_features(app: FastAPI) -> None:
    register_sea(app)
    register_auth(app)
    register_health(app)
    register_api(app)
    register_chat(app)
    register_report(app)


__all__ = ["register_all_features"]
