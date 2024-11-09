from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models import User
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.auth_manager import UserAuthManager
from backend.app.routes.general_models import GeneralHeadersModel
from backend.app.routes.main import MainRouterMIXIN
from backend.app.routes.user.models import *
from backend.app.routes.user.response_models import *

user_router = InferringRouter()
user_tags = ["user_router"]


class UserRouterMIXIN(UserAuthManager, MainRouterMIXIN, ManagerSQLAlchemy):

    @staticmethod
    def get_data_by_response_created(user_profile: User) -> dict:
        return {
            'id': user_profile.id,
            'name': user_profile.name,
            'lastname': user_profile.lastname,
            'phone_number': user_profile.phone_number,
            'email': user_profile.email,
            'vtb_auth': user_profile.vtb_auth,
            'token_auth': user_profile.token_auth
        }


@cbv(user_router)
class UserAuthRouter(UserRouterMIXIN):
    @user_router.get(
        "/auth/",
        name='auth_user',
        response_model=UserResponse,
        responses=auth_responses,
        description='Авторизация',
        tags=user_tags
    )
    async def get(self, request: Request, response: Response, headers: GeneralHeadersModel = Depends()):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            logger.info(headers.authorization)
            if user_profile := await self.authenticate_user(session, None, None, headers.authorization):
                data: dict = self.get_data_by_response_created(user_profile)
                result = self.get_data(data)
                return result

            return self.make_response_by_error()

    @user_router.post(
        "/auth/",
        name='auth_user',
        response_model=UserResponse,
        responses=user_auth_responses,
        description='Аунтефикация',
        tags=user_tags
    )
    async def post(self, request: Request, response: Response, body: UserGETModel):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if user_profile := await self.authenticate_user(session, body.phone_number, body.password, None):
                data: dict = self.get_data_by_response_created(user_profile)
                result = self.get_data(data)
                return result

            return self.make_response_by_error()


@cbv(user_router)
class UserRouter(UserRouterMIXIN):

    @user_router.post(
        "/user/",
        name='create_user',
        response_model=UserCreateResponse,
        responses=user_create_responses,
        description='Создание пользователя',
        tags=user_tags
    )
    async def post(self, request: Request, body: UserModel):
        row_data: dict = {
            'password': self.create_hash_password(body.password),
            'phone_number': body.phone_number,
            'vtb_auth': body.vtb_auth if body.vtb_auth else '',
            'token_auth': self.create_access_token()
        }

        await self.create_user(row_data)
        data: dict = {'code': '0000', 'token_auth': row_data['token_auth']}
        result = self.get_data(data)
        return result

    @user_router.post(
        "/activate_user/",
        name='activate_user',
        response_model=UserResponse,
        responses=user_create_responses,
        description='Подтверждение пользователя',
        tags=user_tags
    )
    async def activate_user(self, request: Request, body: UserActivateModel, headers: GeneralHeadersModel = Depends()):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user_profile_select = await session.execute(select(User).filter_by(token_auth=headers.authorization))
            user_profile: User = user_profile_select.scalars().first()
            if user_profile and body.sms_code == user_profile.sms_code:
                user_profile.is_active = True
                await session.commit()
                return self.get_data_by_response_created(user_profile)

        return self.make_response_by_error()

    @classmethod
    async def create_user(cls, data: dict) -> dict:
        async with AsyncSession(cls.engine, autoflush=False, expire_on_commit=False) as session:
            if user_profile := await cls._check_phone_number_by_user(session, data['phone_number']):
                return cls.get_data_by_response_created(user_profile)

            user_profile: User = User(**data)
            session.add(user_profile)
            await session.commit()
            return cls.get_data_by_response_created(user_profile)

    @staticmethod
    async def _check_phone_number_by_user(session: AsyncSession, phone_number: str) -> User | None:
        user_profile_select = await session.execute(select(User).filter_by(phone_number=phone_number))
        if user_profile := user_profile_select.scalars().first():
            return user_profile

        return None


@cbv(user_router)
class UserDataRouter(UserRouterMIXIN):
    @user_router.post(
        "/user_data/",
        name='create_user_data',
        response_model=UserResponse,
        responses=user_data_responses,
        description='Дополнение данных пользователя',
        tags=user_tags
    )
    async def post(self, request: Request, body: UserDataModel):
        row_data: dict = {
            'name': body.name,
            'lastname': body.lastname,
            'phone_number': body.phone_number,
            'email': body.email if body.email else ''
        }
        if data := await self.create_user_data(row_data):
            result = self.get_data(data)
            return result

        return self.make_response_by_error()

    async def create_user_data(self, data: dict):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user_profile: User = await self._get_user_by_phone_number(session, data['phone_number'])
            if not user_profile:
                return None

            user_profile.name = data['name']
            user_profile.lastname = data['lastname']
            user_profile.email = data['email']
            await session.commit()

            return self.get_data_by_response_created(user_profile)

    @staticmethod
    async def _get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User | None:
        user_profile_select = await session.execute(select(User).filter_by(phone_number=phone_number))
        if user_profile := user_profile_select.scalars().first():
            return user_profile

        return None


@cbv(user_router)
class UserVTBRouter(UserRouterMIXIN):
    @user_router.get(
        "/user_vtb/",
        name='user_vtb',
        response_model=UserResponse,
        responses=user_vtb_responses,
        description='Вход через VTB ID',
        tags=user_tags
    )
    async def get(self, request: Request, response: Response):
        data_by_vtb_user: dict = self.get_data_by_vtb_user()
        data: dict = await self.get_or_create_user(data_by_vtb_user)
        result = self.get_data(data)
        return result

    @classmethod
    async def get_or_create_user(cls, data: dict) -> dict:
        async with AsyncSession(cls.engine, autoflush=False, expire_on_commit=False) as session:
            if user_profile := await cls._get_user_by_phone_number(session, data['phone_number']):
                data: dict = cls.get_data_by_response_created(user_profile)
                result = cls.get_data(data)
                return result

            user_profile: User = User(**data)
            session.add(user_profile)
            await session.commit()

            data: dict = cls.get_data_by_response_created(user_profile)
            result = cls.get_data(data)
            return result

    @staticmethod
    async def _get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User | None:
        user_profile_select = await session.execute(select(User).filter_by(phone_number=phone_number))
        if user_profile := user_profile_select.scalars().first():
            return user_profile

        return None

    @staticmethod
    def get_data_by_vtb_user():
        return {
            'name': 'Иван',
            'lastname': 'Иванов',
            'phone_number': '+79993980790',
            'email': 'ivan@vtb.ru',
            'vtb_auth': 'FeWYgKYSurErBZdexVhoMSjo1DGtvgg9',
            'token_auth': 'FeWYgKYSurErBZdexVhoMSjo1DGtvgg9'
        }
