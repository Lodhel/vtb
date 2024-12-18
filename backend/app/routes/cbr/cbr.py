import datetime

from fastapi import APIRouter, Request, Response, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import InflationGoal, InflationData, KeyRate, InterbankRate, CurrencyRate, MetalPrice, \
    Reserve, LiquidityIndicator, BankRequirement, Inflation
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.cbr.models import CbrParams, ComplexCBR_Response, InflationParams, InflationResponse
from backend.app.routes.cbr.response_models import cbr_responses, inflation_responses
from backend.app.routes.main import MainRouterMIXIN

cbr_router = APIRouter()
cbr_tags = ["cbr_router"]


@cbv(cbr_router)
class CbrRouter(MainRouterMIXIN, ManagerSQLAlchemy):

    @cbr_router.get(
        "/inflation/",
        name='inflation',
        response_model=InflationResponse,
        responses=inflation_responses,
        description='Получение данных по инфляции',
        tags=cbr_tags
    )
    async def get(self, request: Request, response: Response, params: InflationParams = Depends()):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if not params.rate_date:
                result = await session.execute(select(Inflation))
            else:
                rate_date = datetime.datetime.strptime(params.rate_date, "%Y-%m-%d").date()
                result = await session.execute(select(Inflation).filter(Inflation.is_date == rate_date))

            data = result.scalars().all()
            return self.get_data(
                [
                    self.get_data_by_response_created(inflation) for inflation in data
                ]
            )

    @staticmethod
    def get_data_by_response_created(inflation: Inflation) -> dict:
        return {
            'id': inflation.id,
            'is_date': inflation.is_date.strftime('%Y-%m-%d'),
            'rate': float(inflation.rate),
            'inflation_rate': float(inflation.inflation_rate)
        }


@cbv(cbr_router)
class CbrRouter(MainRouterMIXIN, ManagerSQLAlchemy):

    @cbr_router.get(
        "/cbr/",
        name='cbr',
        response_model=ComplexCBR_Response,
        responses=cbr_responses,
        description='Получение данных по ЦБ',
        tags=cbr_tags
    )
    async def get(self, request: Request, response: Response, params: CbrParams = Depends()):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if not params.rate_date:
                rate_date = datetime.date.today()
            else:
                rate_date = datetime.datetime.strptime(params.rate_date, "%Y-%m-%d").date()
            data = await self.get_data_by_response_created(session, rate_date)
            return data

    @staticmethod
    async def get_data_by_response_created(session: AsyncSession, rate_date) -> dict:
        data: dict = {}
        models = [
            (InflationGoal, "inflation_goal"),
            (InflationData, "inflation_data"),
            (KeyRate, "key_rate"),
            (InterbankRate, "interbank_rate"),
            (CurrencyRate, "currency_rate"),
            (MetalPrice, "metal_price"),
            (Reserve, "reserve"),
            (LiquidityIndicator, "liquidity_indicator"),
            (BankRequirement, "bank_requirement")
        ]

        for model, model_name in models:
            result = await session.execute(select(model).filter(model.is_date == rate_date))
            model_data = result.scalars().all()
            data[model_name] = [item.__dict__ for item in model_data]

        return data

