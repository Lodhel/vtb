import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class CurrencyType(str, Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    CNY = "CNY"


class AccumulatedAccountCreate(BaseModel):
    amount: Optional[float] = Field(0.0, description="Сумма на счете, по умолчанию 0")
    currency: CurrencyType = Field(CurrencyType.RUB, description="Валюта счета (RUB, USD, EUR, CNY)")

    class Config:
        orm_mode = True


class AccumulatedAccountInvite(BaseModel):
    account_id: int = Field(..., description="ID накопительного счета")
    invited_user_id: int = Field(..., description="ID пользователя, которого приглашают к счету")


class BalanceOperation(BaseModel):
    account_id: int = Field(..., description="ID накопительного счета")
    amount: float = Field(..., description="Сумма для операции (пополнения или списания)")


class AccumulatedAccountData(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор счета")
    owner_id: int = Field(..., description="ID владельца счета")
    amount: float = Field(..., description="Текущая сумма на счете")
    currency: CurrencyType = Field(..., description="Валюта счета")
    created_at: datetime.datetime = Field(..., description="Дата создания счета")

    class Config:
        orm_mode = True


class AccumulatedAccountResponse(BaseModel):
    data: List[AccumulatedAccountData] = Field(..., description="Список накопительных счетов")

    class Config:
        orm_mode = True
