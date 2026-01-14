from fastapi import FastAPI
from src.features.report.report_route import report_router

def register_feature(app: FastAPI) -> None:
    app.include_router(report_router, prefix="/report", tags=["Report"])
