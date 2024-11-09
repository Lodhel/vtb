from fastapi import Query
from pydantic import BaseModel


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
    amount: AmountResponse
    creditDebitIndicator: str
    type: str


class CardResponse(BaseModel):
    accountId: str
    balance: BalanceResponse
    creditDebitIndicator: str
    type: str

