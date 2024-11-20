from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.app.models import AccumulatedAccount, User, accumulated_account_invitations, InvitationStatus
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.accumulated_accounts.accumulated_accounts_schemas import AccumulatedAccountSchema
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
    async def get_data_by_response_created(session: AsyncSession, account_model: AccumulatedAccount) -> dict:
        invitations_query = await session.execute(
            select(
                accumulated_account_invitations.c.invited_user_id,
                accumulated_account_invitations.c.role,
                accumulated_account_invitations.c.status
            ).where(accumulated_account_invitations.c.account_id == account_model.id)
        )
        invitations = invitations_query.fetchall()

        # 2. Получение списка ID приглашённых пользователей
        invited_user_ids = [row.invited_user_id for row in invitations]

        # 3. Загрузка данных о пользователях
        invited_users_query = await session.execute(
            select(User).where(User.id.in_(invited_user_ids))
        )
        invited_users = invited_users_query.scalars().all()

        # 4. Соединение пользователей с их ролями и статусами
        invited_users_with_roles = [
            {
                "name": user.name,
                "lastname": user.lastname,
                "role": next((row.role.value for row in invitations if row.invited_user_id == user.id), None),
                "status": next((row.status.value for row in invitations if row.invited_user_id == user.id), None),
            }
            for user in invited_users
        ]

        # 5. Загрузка владельца
        await session.refresh(account_model, ["owner"])

        # 6. Формирование финального ответа
        return {
            'id': account_model.id,
            'owner_id': account_model.owner_id,
            'amount': float(account_model.amount),
            'currency': account_model.currency.value,
            'account_type': account_model.account_type.value,
            'created_at': account_model.created_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'users': {
                "owner": {
                    "name": account_model.owner.name,
                    "lastname": account_model.owner.lastname,
                },
                "invited_users": invited_users_with_roles,
            }
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
                    await self.get_data_by_response_created(session, account) for account in accounts
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
                data: dict = await self.get_data_by_response_created(session, accumulated_account)
                return self.get_data(data)

            return self.make_response_by_error()

    @accumulated_accounts_router.post(
        "/accumulated_accounts/invite",
        name='invite_to_accumulated_account',
        response_model=AccumulatedAccountInviteData,
        responses=accumulated_account_responses,
        description='Приглашение другого пользователя в счёт',
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
                    phone_number=body.invited_user_phone
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
                    invited_user_id=invited_user.id,
                    role=body.role
                )
            )
            await session.flush()
            await session.commit()

            return self.get_data({
                'id': account.id,
                'success': True
            })

    @accumulated_accounts_router.post(
        "/accumulated_accounts/invite/confirm",
        name='confirm_invite_to_accumulated_account',
        response_model=AccumulatedAccountData,
        responses=accumulated_account_responses,
        description='Подтверждение или отклонение приглашения на счёт',
        tags=accumulated_accounts_tags
    )
    async def confirm_invite(
        self,
        body: ConfirmInviteRequest,
        headers: GeneralHeadersModel = Depends()
    ):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            user = await self.authenticate_user(session, None, None, headers.authorization)
            if not user:
                return self.make_response_by_error()

            account_select = await session.execute(
                select(
                    AccumulatedAccount
                ).filter_by(id=body.account_id)
            )
            account = account_select.scalars().first()
            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Accumulated account not found"
                )

            invite_check = await session.execute(
                select(
                    accumulated_account_invitations
                ).where(
                    accumulated_account_invitations.c.account_id == body.account_id,
                    accumulated_account_invitations.c.invited_user_id == user.id
                )
            )
            invite = invite_check.scalars().first()

            if not invite:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You were not invited to this account"
                )

            if body.action == "confirm":
                new_status = InvitationStatus.CONFIRMED
            elif body.action == "reject":
                new_status = InvitationStatus.REJECTED
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid action. Use 'confirm' or 'reject'"
                )

            await session.execute(
                accumulated_account_invitations.update().where(
                    accumulated_account_invitations.c.account_id == body.account_id,
                    accumulated_account_invitations.c.invited_user_id == user.id
                ).values(
                    status=new_status
                )
            )
            await session.flush()
            await session.commit()

            if body.action == "confirm":
                data = await self.get_data_by_response_created(session, account)
            elif body.action == "reject":
                data = {
                    'success': True,
                    'action': 'reject'
                }
            return self.get_data(data)

    @accumulated_accounts_router.post(
        "/accumulated_accounts/deposit",
        name='deposit_to_account',
        response_model=AccumulatedAccountData,
        responses=accumulated_account_responses,
        description='Начисление средств на счёт',
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

            await self.check_permissions(
                AccumulatedAccountSchema(**{
                    'session': session,
                    'owner_id': account.owner_id,
                    'user_id': user.id,
                    'account_id': body.account_id,
                    'permissions_list': [UserRole.CONTRIBUTOR, UserRole.FULL_ACCESS]
                })
            )
            account.amount += body.amount
            await session.commit()

            data = await self.get_data_by_response_created(session, account)
            return self.get_data(data)

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

            await self.check_permissions(
                AccumulatedAccountSchema(**{
                    'session': session,
                    'owner_id': account.owner_id,
                    'user_id': user.id,
                    'account_id': body.account_id,
                    'permissions_list': [UserRole.FULL_ACCESS, ]
                })
            )

            if account.amount < body.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds"
                )

            account.amount -= body.amount
            await session.commit()

            data = await self.get_data_by_response_created(session, account)
            return self.get_data(data)

    @staticmethod
    async def check_permissions(accumulated_account_schema: AccumulatedAccountSchema) -> None:
        if accumulated_account_schema.owner_id != accumulated_account_schema.user_id:
            user_role_select = await accumulated_account_schema.session.execute(
                select(
                    accumulated_account_invitations.c.role
                ).where(
                    accumulated_account_invitations.c.account_id == accumulated_account_schema.account_id,
                    accumulated_account_invitations.c.invited_user_id == accumulated_account_schema.user_id
                )
            )
            user_role = user_role_select.scalars().first()

            if user_role not in accumulated_account_schema.permissions_list:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No permission to operation to this account"
                )
