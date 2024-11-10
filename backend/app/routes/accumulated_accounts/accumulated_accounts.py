from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.app.models import AccumulatedAccount, User, accumulated_account_invitations
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.accumulated_accounts.models import *
from backend.app.routes.accumulated_accounts.response_models import accumulated_accounts_responses, \
    accumulated_account_responses
from backend.app.routes.auth_manager import UserAuthManager
from backend.app.routes.general_models import GeneralHeadersModel
from backend.app.routes.main import MainRouterMIXIN

accumulated_accounts_router = APIRouter()
accumulated_accounts_tags = ["accumulated_accounts_router"]


class AccumulatedAccountMIXIN(UserAuthManager, MainRouterMIXIN, ManagerSQLAlchemy):

    @staticmethod
    def get_data_by_response_created(account_model: AccumulatedAccount) -> dict:
        return {
            'id': account_model.id,
            'owner_id': account_model.owner_id,
            'amount': float(account_model.amount),
            'currency': account_model.currency.value,
            'created_at': account_model.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        }


@cbv(accumulated_accounts_router)
class AccumulatedAccountRouter(AccumulatedAccountMIXIN):

    @accumulated_accounts_router.get(
        "/accumulated_accounts/",
        name='accumulated_accounts',
        response_model=AccumulatedAccountResponse,
        responses=accumulated_accounts_responses,
        description='Получение списка накопительных счетов пользователя',
        tags=accumulated_accounts_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if user := await self.authenticate_user(session, None, None, headers.authorization):
                accounts_select = await session.execute(
                    select(
                        AccumulatedAccount
                    ).outerjoin(
                        accumulated_account_invitations,
                        AccumulatedAccount.id == accumulated_account_invitations.c.account_id
                    ).where(
                        or_(
                            AccumulatedAccount.owner_id == user.id,
                            accumulated_account_invitations.c.invited_user_id == user.id
                        )
                    )
                )
                accounts = accounts_select.scalars().all()
                data: List[dict] = [
                    self.get_data_by_response_created(account) for account in accounts
                ]
                return self.get_data(data)

            return self.make_response_by_error()

    @accumulated_accounts_router.post(
        "/accumulated_accounts/",
        name='create_accumulated_account',
        response_model=AccumulatedAccountData,
        responses=accumulated_account_responses,
        description='Создание нового накопительного счета',
        tags=accumulated_accounts_tags
    )
    async def post(
        self,
        request: Request,
        response: Response,
        body: AccumulatedAccountCreate,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if user := await self.authenticate_user(session, None, None, headers.authorization):
                accumulated_account = AccumulatedAccount(
                    owner_id=user.id,
                    amount=body.amount,
                    currency=body.currency
                )
                session.add(accumulated_account)
                await session.commit()
                await session.refresh(accumulated_account)
                data: dict = self.get_data_by_response_created(accumulated_account)
                return self.get_data(data)

            return self.make_response_by_error()

    @accumulated_accounts_router.post(
        "/accumulated_accounts/invite",
        name='invite_to_accumulated_account',
        response_model=AccumulatedAccountData,
        responses=accumulated_account_responses,
        description='Приглашение другого пользователя в накопительный счёт',
        tags=accumulated_accounts_tags
    )
    async def invite_user(
        self,
        body: AccumulatedAccountInvite,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            account_select = await session.execute(
                select(
                    AccumulatedAccount
                ).filter_by(
                    id=body.account_id
                )
            )
            account = account_select.scalars().first()
            if not account or account.owner_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No permission to invite users to this account"
                )

            invited_user_select = await session.execute(
                select(
                    User
                ).filter_by(
                    id=body.invited_user_id
                )
            )
            invited_user = invited_user_select.scalars().first()
            if not invited_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User to invite not found"
                )

            await session.execute(
                accumulated_account_invitations.insert().values(
                    account_id=account.id,
                    invited_user_id=invited_user.id
                )
            )
            await session.flush()
            await session.commit()

            return self.get_data_by_response_created(account)

    @accumulated_accounts_router.post(
        "/accumulated_accounts/deposit",
        name='deposit_to_account',
        response_model=AccumulatedAccountData,
        responses=accumulated_account_responses,
        description='Начисление средств на накопительный счёт',
        tags=accumulated_accounts_tags
    )
    async def deposit(
        self,
        body: BalanceOperation,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            account_select = await session.execute(
                select(
                    AccumulatedAccount
                ).outerjoin(
                    accumulated_account_invitations,
                    AccumulatedAccount.id == accumulated_account_invitations.c.account_id
                ).where(
                    AccumulatedAccount.id == body.account_id,
                    or_(
                        AccumulatedAccount.owner_id == user.id,
                        accumulated_account_invitations.c.invited_user_id == user.id
                    )
                )
            )
            account = account_select.scalars().first()
            if not account:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No permission to deposit to this account"
                )

            account.amount += body.amount
            await session.commit()

            return self.get_data_by_response_created(account)

    @accumulated_accounts_router.post(
        "/accumulated_accounts/withdraw",
        name='withdraw_from_account',
        response_model=AccumulatedAccountData,
        responses=accumulated_account_responses,
        description='Снятие средств с накопительного счёта',
        tags=accumulated_accounts_tags
    )
    async def withdraw(
        self,
        body: BalanceOperation,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            account_select = await session.execute(
                select(
                    AccumulatedAccount
                ).outerjoin(
                    accumulated_account_invitations,
                    AccumulatedAccount.id == accumulated_account_invitations.c.account_id
                ).where(
                    AccumulatedAccount.id == body.account_id,
                    or_(
                        AccumulatedAccount.owner_id == user.id,
                        accumulated_account_invitations.c.invited_user_id == user.id
                    )
                )
            )
            account = account_select.scalars().first()
            if not account:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No permission to withdraw from this account"
                )

            if account.amount < body.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds"
                )

            account.amount -= body.amount
            await session.commit()

            return self.get_data_by_response_created(account)
