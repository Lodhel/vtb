from fastapi import APIRouter

from backend.app.routes.accumulated_accounts.accumulated_accounts import accumulated_accounts_router
from backend.app.routes.card.card import card_router
from backend.app.routes.cars.cars import car_router
from backend.app.routes.cbr.cbr import cbr_router
from backend.app.routes.currency.currency import currency_router
from backend.app.routes.recommended_deposits.recommended_deposits import recommended_deposit_router
from backend.app.routes.saving_goals.saving_goals import goal_router
from backend.app.routes.user.user_router import user_router
from backend.app.routes.user_profile.user_profile import user_profile_router

router = APIRouter()
router.include_router(user_router)
router.include_router(user_profile_router)
router.include_router(recommended_deposit_router)
router.include_router(accumulated_accounts_router)
router.include_router(goal_router)
router.include_router(card_router)
router.include_router(cbr_router)
router.include_router(currency_router)
router.include_router(car_router)


__all__ = ["router"]
