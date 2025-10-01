from fastapi import APIRouter
from src.controller.auth_controller import router as auth_controller

router = APIRouter(prefix="/auth", tags=["Auth"])
router.include_router(auth_controller)
