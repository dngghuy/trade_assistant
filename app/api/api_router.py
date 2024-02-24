from fastapi import APIRouter
from app.api import (
    api_healthcheck,
    api_stock_price_info
)

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")
router.include_router(api_stock_price_info.router, tags=["stockInfo"], prefix="/stockInfo")
