from fastapi import APIRouter, Request, Response, Depends
from fastapi_utils.cbv import cbv

from backend.app.routes.card.models import CardResponse, CardParams
from backend.app.routes.card.response_models import card_responses
from backend.app.routes.main import MainRouterMIXIN
from backend.app.vtb_services.accounts_manager import VTB_AccountsManager

card_router = APIRouter()
card_tags = ["card_router"]


@cbv(card_router)
class CarRouter(MainRouterMIXIN):

    def __init__(self):
        self.vtb_account_manager = VTB_AccountsManager()

    @card_router.get(
        "/card/",
        name='card',
        response_model=CardResponse,
        responses=card_responses,
        description='Получение баланса карты пользователя',
        tags=card_tags
    )
    async def get(self, request: Request, response: Response, params: CardParams = Depends()):
        return await self.vtb_account_manager.get_balance(params.account_id)
