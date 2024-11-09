from fastapi import APIRouter

from backend.app.routes.card.card import card_router
from backend.app.routes.cars.cars import car_router
from backend.app.routes.cbr.cbr import cbr_router
from backend.app.routes.user.user_router import user_router

router = APIRouter()
router.include_router(user_router)
router.include_router(card_router)
router.include_router(cbr_router)
router.include_router(car_router)


__all__ = ["router"]
