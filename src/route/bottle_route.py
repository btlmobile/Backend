from fastapi import APIRouter
from src.controller.bottle_controller import router as bottle_controller

router = APIRouter(prefix="/api", tags=["Api"])
router.include_router(bottle_controller)
