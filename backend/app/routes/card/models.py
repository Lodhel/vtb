from fastapi import Query
from pydantic import BaseModel
from typing import Dict


class CardParams:
    def __init__(
        self,
        account_id: str = Query(default='a502db73-0c2c-483b-b7b7-cb8393221698', description="accountId")
    ):
        self.account_id = account_id


class AmountResponse(BaseModel):
    currency: str
    amount: str


class BalanceResponse(BaseModel):
    balance: Dict[AmountResponse]


class CardResponse(BaseModel):
    accountId: str
    balance: Dict[BalanceResponse]
    creditDebitIndicator: str
    type: str
