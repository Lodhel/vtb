import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

from backend.app.models import UserRole, AccumulatedAccount


class AccumulatedAccountCreate(BaseModel):
    amount: Optional[float] = Field(0.0, description="Сумма на счете, по умолчанию 0")
    currency: AccumulatedAccount.CurrencyType = Field(
        AccumulatedAccount.CurrencyType.RUB,
        description="Валюта счета (RUB, USD, EUR, CNY)"
    )
    account_type: AccumulatedAccount.AccountType = Field(
        AccumulatedAccount.AccountType.PERSONAL,
        description="Тип счета (Личный, Совместный, Счет для детей, Краудфандинг, Инвестиционный, Социальный)"
    )

    class Config:
        orm_mode = True


class AccumulatedAccountInvite(BaseModel):
    account_id: int = Field(..., description="ID накопительного счета")
    invited_user_phone: str = Field(..., description="Телефон пользователя, которого приглашают к счету")
    role: UserRole = Field(default=UserRole.VIEWER, description="Роль приглашенного пользователя")


class ConfirmInviteRequest(BaseModel):
    account_id: int = Field(..., description="ID накопительного счета")
    action: str = Field(..., description="Действие: confirm или reject")


class BalanceOperation(BaseModel):
    account_id: int = Field(..., description="ID накопительного счета")
    amount: float = Field(..., description="Сумма для операции (пополнения или списания)")


class UserData(BaseModel):
    name: str = Field(..., description="Имя пользователя")
    lastname: str = Field(..., description="Фамилия пользователя")
    role: Optional[str] = Field(None, description="Роль пользователя в счете")
    status: Optional[str] = Field(None, description="Статус приглашения пользователя")


class OwnerData(BaseModel):
    name: str = Field(..., description="Имя пользователя")
    lastname: str = Field(..., description="Фамилия пользователя")


class AccumulatedAccountData(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор счета")
    owner_id: int = Field(..., description="ID владельца счета")
    amount: float = Field(..., description="Текущая сумма на счете")
    currency: AccumulatedAccount.CurrencyType = Field(..., description="Валюта счета")
    account_type: AccumulatedAccount.AccountType = Field(..., description="Тип счета")
    created_at: datetime.datetime = Field(..., description="Дата создания счета")
    owner: OwnerData = Field(..., description="Данные владельца счета")
    invited_users: List[UserData] = Field(..., description="Список приглашённых пользователей с их ролями и статусами")

    class Config:
        orm_mode = True


class AccumulatedAccountInviteData(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор счета")
    success: bool = Field(..., description="Успешность запроса")


class AccumulatedAccountResponse(BaseModel):
    data: List[AccumulatedAccountData] = Field(..., description="Список накопительных счетов")

    class Config:
        orm_mode = True
