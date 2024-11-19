from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
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
    def get_data_by_response_created(user: User) -> dict:
        return {
            'id': user.id,
            'name': user.name if user.name else '',
            'lastname': user.lastname if user.lastname else '',
            'phone_number': user.phone_number,
            'email': user.email if user.email else '',
            'vtb_auth': user.vtb_auth,
            'token_auth': user.token_auth
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
            if user := await self.authenticate_user(session, None, None, headers.authorization):
                data: dict = self.get_data_by_response_created(user)
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
            if user := await self.authenticate_user(session, body.phone_number, body.password, None):
                data: dict = self.get_data_by_response_created(user)
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
            user: User | None = await self.authenticate_user(session, None, None, headers.authorization)
            if user and body.sms_code == user.sms_code:
                user.is_active = True
                await session.commit()
                return self.get_data(self.get_data_by_response_created(user))

        return self.make_response_by_error()

    @classmethod
    async def create_user(cls, data: dict) -> dict:
        async with AsyncSession(cls.engine, autoflush=False, expire_on_commit=False) as session:
            if user := await cls._check_phone_number_by_user(session, data['phone_number']):
                return cls.get_data_by_response_created(user)

            user: User = User(**data)
            session.add(user)
            await session.commit()
            return cls.get_data_by_response_created(user)

    @staticmethod
    async def _check_phone_number_by_user(session: AsyncSession, phone_number: str) -> User | None:
        user_select = await session.execute(select(User).filter_by(phone_number=phone_number))
        if user := user_select.scalars().first():
            return user

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
            user: User = await self._get_user_by_phone_number(session, data['phone_number'])
            if not user:
                return None

            user.name = data['name']
            user.lastname = data['lastname']
            user.email = data['email']
            await session.commit()

            return self.get_data_by_response_created(user)

    @staticmethod
    async def _get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User | None:
        user_select = await session.execute(select(User).filter_by(phone_number=phone_number))
        if user := user_select.scalars().first():
            return user

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
    async def get(self, request: Request, response: Response, headers: GeneralHeadersModel = Depends()):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if user := await self.authenticate_user(session, None, None, headers.authorization):
                data: dict = self.get_data_by_response_created(user)
                result = self.get_data(data)
                return result

        return self.make_response_by_error()
