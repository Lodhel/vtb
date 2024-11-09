import datetime

from fastapi import APIRouter, Request, Response, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Currency
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.currency.models import CurrencyParams, CurrencyResponse
from backend.app.routes.currency.response_models import currency_responses
from backend.app.routes.main import MainRouterMIXIN

currency_router = APIRouter()
currency_tags = ["currency_router"]


@cbv(currency_router)
class CurrencyRouter(MainRouterMIXIN, ManagerSQLAlchemy):

    @currency_router.get(
        "/currency/",
        name='currency',
        response_model=CurrencyResponse,
        responses=currency_responses,
        description='Получение данных по валютам',
        tags=currency_tags
    )
    async def get(self, request: Request, response: Response, params: CurrencyParams = Depends()):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions is not None:
                currencies_select = await session.execute(select(Currency).filter(conditions))
            else:
                currencies_select = await session.execute(select(Currency))
            currencies = currencies_select.scalars().all()
            data: list = [
                self._get_data_by_response_created(currency) for currency in currencies
            ]
            return self.get_data(data)

    @staticmethod
    def make_conditions(params: CurrencyParams):
        conditions: list = []

        if params.rate_date:
            rate_date = datetime.datetime.strptime(params.rate_date, "%Y-%m-%d").date()
            conditions.append(Currency.is_date == rate_date)

        if params.currency_type:
            conditions.append(Currency.currency_type == params.currency_type)

        return and_(*conditions) if conditions else None

    @staticmethod
    def _get_data_by_response_created(currency_model: Currency) -> dict:
        return {
            'id': currency_model.id,
            'is_date': currency_model.is_date.strftime('%Y-%m-%d'),
            'rate': float(currency_model.rate),
            'currency_type': currency_model.currency_type
        }
