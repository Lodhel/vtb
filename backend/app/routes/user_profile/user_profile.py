import json
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.event_manager.manager_kafka import ManagerKafka
from backend.app.models import UserProfile, User
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.auth_manager import UserAuthManager
from backend.app.routes.general_models import GeneralHeadersModel
from backend.app.routes.main import MainRouterMIXIN
from backend.app.routes.user_profile.models import *
from backend.app.routes.user_profile.response_models import user_profile_responses

user_profile_router = APIRouter()
user_profile_tags = ["user_profile_router"]


@cbv(user_profile_router)
class UserVTBRouter(UserAuthManager, MainRouterMIXIN, ManagerSQLAlchemy):

    @user_profile_router.get(
        "/user_profile/",
        name="user_profile",
        response_model=UserProfileResponse,
        responses=user_profile_responses,
        description="Получение анкеты пользователя",
        tags=user_profile_tags
    )
    async def get(self, request: Request, response: Response, headers: GeneralHeadersModel = Depends()):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user: User | None = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            profile_query = await session.execute(select(UserProfile).filter_by(user_id=user.id))
            profile = profile_query.scalars().first()

            if profile:
                data: dict = self.get_data_by_response_created(profile)
            else:
                data: dict = {
                    "error": "User profile does not exist. Please create a profile."
                }

            result = self.get_data(data)
            return result

    @user_profile_router.post(
        "/user_profile/",
        name="user_profile",
        response_model=UserProfileResponse,
        responses=user_profile_responses,
        description="Заполнение анкеты пользователя",
        tags=user_profile_tags
    )
    async def post(
        self,
        request: Request,
        response: Response,
        body: UserProfileRequest,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user: User | None = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            profile_query = await session.execute(select(UserProfile).filter_by(user_id=user.id))
            profile = profile_query.scalars().first()

            if profile:
                profile.income_last_month = body.income_last_month
                profile.expenses_last_month = body.expenses_last_month
                profile.savings_last_month = body.savings_last_month
                profile.marital_status = body.marital_status
                profile.children_count = body.children_count
                profile.education = body.education
                profile.occupation = body.occupation
            else:
                profile = UserProfile(
                    user_id=user.id,
                    income_last_month=body.income_last_month,
                    expenses_last_month=body.expenses_last_month,
                    savings_last_month=body.savings_last_month,
                    marital_status=body.marital_status,
                    children_count=body.children_count,
                    education=body.education,
                    occupation=body.occupation
                )
                session.add(profile)

            await session.commit()
            data = self.get_data_by_response_created(profile)

            async with ManagerKafka().producer as producer:
                message_to_produce = json.dumps(data).encode(encoding="utf-8")
                await producer.send(value=message_to_produce)

            result = self.get_data(data)
            return result

    @staticmethod
    def get_data_by_response_created(profile: UserProfile) -> dict:
        return {
            'user_id': profile.user_id,
            'income_last_month': profile.income_last_month,
            'expenses_last_month': profile.expenses_last_month,
            'savings_last_month': profile.savings_last_month,
            'marital_status': profile.marital_status,
            'children_count': profile.children_count,
            'education': profile.education.value,
            'occupation': profile.occupation.value
        }
