from datetime import datetime

from fastapi import APIRouter, Request, Response, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import RecommendedDeposit, User
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.auth_manager import UserAuthManager
from backend.app.routes.general_models import GeneralHeadersModel
from backend.app.routes.main import MainRouterMIXIN
from backend.app.routes.recommended_deposits.models import RecommendedDepositParams, RecommendedDepositResponse
from backend.app.routes.recommended_deposits.response_models import recommended_deposits_responses

recommended_deposit_router = APIRouter()
recommended_deposit_tags = ["recommended_deposit_router"]


@cbv(recommended_deposit_router)
class RecommendedDepositRouter(UserAuthManager, MainRouterMIXIN, ManagerSQLAlchemy):

    @recommended_deposit_router.get(
        "/recommended-deposits/",
        name='recommended_deposits',
        response_model=RecommendedDepositResponse,
        responses=recommended_deposits_responses,
        description='Получение рекомендованного депозита за месяц',
        tags=recommended_deposit_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        params: RecommendedDepositParams = Depends(),
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user: User | None = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            conditions = self.make_conditions(params, user.id)
            if conditions is not None:
                deposits_select = await session.execute(select(RecommendedDeposit).filter(conditions))
            else:
                deposits_select = await session.execute(select(RecommendedDeposit))

            deposit: RecommendedDeposit | None = deposits_select.scalars().first()
            result = self.get_data(self.get_data_by_response_created(deposit))
            return result

    @staticmethod
    def make_conditions(params: RecommendedDepositParams, user_id):
        conditions = []
        if user_id is not None:
            conditions.append(RecommendedDeposit.user_id == user_id)

        if params.rate_date:
            try:
                rate_date = datetime.strptime(params.rate_date, "%Y-%m").date()
                conditions.append(RecommendedDeposit.rate_date == rate_date)
            except ValueError:
                raise ValueError("Неверный формат даты. Ожидается формат: YYYY-MM")
        else:
            now = datetime.now()
            current_month_date = datetime.strptime(f"{now.year}-{now.month}", "%Y-%m").date()
            conditions.append(RecommendedDeposit.rate_date == current_month_date)

        return and_(*conditions) if conditions else None

    @staticmethod
    def get_data_by_response_created(deposit: RecommendedDeposit | None) -> dict:
        if deposit:
            return {
                'recommended_deposit': deposit.recommended_deposit,
                'rate_date': deposit.rate_date.strftime("%Y-%m")
            }
        else:
            now = datetime.now()
            return {
                'recommended_deposit': 0.0,
                'rate_date': f"{now.year}-{now.month}"
            }
