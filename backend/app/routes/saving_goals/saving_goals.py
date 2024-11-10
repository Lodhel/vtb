from fastapi import Depends, HTTPException, Request, Response, APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.models import User, AccumulatedAccount, SavingGoal
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.auth_manager import UserAuthManager
from backend.app.routes.general_models import GeneralHeadersModel
from backend.app.routes.main import MainRouterMIXIN
from backend.app.routes.saving_goals.models import GoalResponse, GoalRequest
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
    async def get(self, request: Request, response: Response, headers: GeneralHeadersModel = Depends()):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user: User | None = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            goal_query = await session.execute(select(SavingGoal).filter_by(user_id=user.id))
            goal = goal_query.scalars().first()
            if not goal:
                raise HTTPException(status_code=404, detail="Saving goal not found")

            return GoalResponse(
                description=goal.description,
                target_amount=goal.target_amount,
                recommended_contribution=goal.recommended_contribution,
                progress_percentage=goal.progress_percentage
            )

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
        goal_request: GoalRequest,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user: User | None = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            account_query = await session.execute(select(AccumulatedAccount).filter_by(owner_id=user.id))
            account = account_query.scalars().first()
            if not account:
                raise HTTPException(status_code=404, detail="Accumulated account not found")

            recommended_contribution = self.calculate_recommended_contribution(
                goal_request.target_amount, account.amount, goal_request.months_remaining
            )
            progress_percentage = self.calculate_progress(account.amount, goal_request.target_amount)

            goal = SavingGoal(
                user_id=user.id,
                account_id=account.id,
                description=goal_request.description,
                target_amount=goal_request.target_amount,
                recommended_contribution=recommended_contribution,
                progress_percentage=progress_percentage
            )

            session.add(goal)
            await session.commit()
            await session.refresh(goal)

            data = self.get_data_by_response_created(goal)
            return self.get_data(data)

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
        return {
            "description": goal.description,
            "target_amount": goal.target_amount,
            "recommended_contribution": goal.recommended_contribution,
            "progress_percentage": goal.progress_percentage
        }
