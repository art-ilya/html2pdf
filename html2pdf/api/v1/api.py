from fastapi import APIRouter
from .endpoints import convert_request

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(convert_request.router)
