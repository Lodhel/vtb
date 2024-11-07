from fastapi import APIRouter

from backend.app.routes.cars.cars import car_router
from backend.app.routes.cbr.cbr import cbr_router

router = APIRouter()
router.include_router(car_router)
router.include_router(cbr_router)


__all__ = ["router"]
