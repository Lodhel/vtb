import datetime

from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class CurrencyType(str, Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    CNY = "CNY"


class AccumulatedAccountCreate(BaseModel):
    amount: Optional[float] = 0.0
    currency: CurrencyType = CurrencyType.RUB

    class Config:
        orm_mode = True


class AccumulatedAccountInvite(BaseModel):
    account_id: int
    invited_user_id: int


class BalanceOperation(BaseModel):
    account_id: int
    amount: float


class AccumulatedAccountData(BaseModel):
    id: int
    owner_id: int
    amount: float
    currency: CurrencyType
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class AccumulatedAccountResponse(BaseModel):
    data: List[AccumulatedAccountData]

    class Config:
        orm_mode = True
