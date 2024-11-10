from fastapi import Depends, HTTPException, Request, Response, APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from datetime import date
from dateutil.relativedelta import relativedelta

from backend.app.models import User, AccumulatedAccount, SavingGoal
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.auth_manager import UserAuthManager
from backend.app.routes.general_models import GeneralHeadersModel
from backend.app.routes.main import MainRouterMIXIN
from backend.app.routes.saving_goals.models import *
from backend.app.routes.saving_goals.response_models import user_goal_responses

goal_router = APIRouter()
goal_tags = ["goal_router"]


@cbv(goal_router)
class SavingGoalCBV(UserAuthManager, MainRouterMIXIN, ManagerSQLAlchemy):

    @goal_router.get(
        "/goal",
        name='goal',
        response_model=GoalResponse,
        responses=user_goal_responses,
        description='Получение информации по поставленной цели',
        tags=goal_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        params: GoalParams = Depends(),
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user: User | None = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            account = await self.get_account(session, user.id, params.account_id)
            if not account:
                raise HTTPException(status_code=404, detail="Accumulated account not found")

            goal_query = await session.execute(
                select(
                    SavingGoal
                ).filter_by(
                    account_id=account.id
                )
            )
            goal = goal_query.scalars().first()
            if not goal:
                raise HTTPException(status_code=404, detail="Saving goal not found")

            data = self.get_data_by_response_created(goal)
            return self.get_data(data)

    @goal_router.post(
        "/goal",
        name='goal',
        response_model=GoalResponse,
        responses=user_goal_responses,
        description='Указать информацию по поставленной цели',
        tags=goal_tags
    )
    async def post(
        self,
        request: Request,
        response: Response,
        body: GoalRequest,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user: User | None = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            account = await self.get_account(session, user.id, body.account_id)
            if not account:
                raise HTTPException(status_code=404, detail="Accumulated account not found")

            recommended_contribution = self.calculate_recommended_contribution(
                body.target_amount, account.amount, body.months_remaining
            )
            progress_percentage = self.calculate_progress(account.amount, body.target_amount)

            goal = SavingGoal(
                user_id=user.id,
                account_id=account.id,
                description=body.description,
                target_amount=body.target_amount,
                recommended_contribution=recommended_contribution,
                progress_percentage=progress_percentage
            )

            session.add(goal)
            await session.commit()
            await session.refresh(goal)

            data = self.get_data_by_response_created(goal)
            return self.get_data(data)

    @staticmethod
    async def get_account(session: AsyncSession, user_id: int, account_id: int) -> AccumulatedAccount | None:
        account_query = await session.execute(
            select(
                AccumulatedAccount
            ).filter(
                or_(
                    AccumulatedAccount.owner_id == user_id,
                    AccumulatedAccount.invited_users.any(id=user_id)
                )
            ).filter_by(
                id=account_id
            )
        )
        return account_query.scalars().first()

    @staticmethod
    def calculate_progress(account_amount: float, target_amount: float) -> float:
        if target_amount > 0:
            return (account_amount / target_amount) * 100
        return 0.0

    @staticmethod
    def calculate_recommended_contribution(target_amount: float, account_amount: float, months_remaining: int) -> float:
        if months_remaining > 0:
            return (target_amount - account_amount) / months_remaining
        return 0.0

    @staticmethod
    def get_data_by_response_created(goal: SavingGoal) -> dict:
        rate_date = date.today() + relativedelta(months=goal.months_remaining)
        return {
            "description": goal.description,
            "target_amount": goal.target_amount,
            "recommended_contribution": goal.recommended_contribution,
            "progress_percentage": goal.progress_percentage,
            "rate_date": rate_date.strftime("%Y-%m-%d")
        }
