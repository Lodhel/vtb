from fastapi import Query
from pydantic import BaseModel, Field


class CardParams:
    def __init__(
        self,
        account_id: str = Query(
            default='a502db73-0c2c-483b-b7b7-cb8393221698',
            description="Уникальный идентификатор счета пользователя (accountId)"
        )
    ):
        self.account_id = account_id


class AmountResponse(BaseModel):
    currency: str = Field(..., description="Валюта счета, например, RUB, USD")
    amount: str = Field(..., description="Сумма на счете в указанной валюте")


class BalanceResponse(BaseModel):
    amount: AmountResponse = Field(..., description="Детали суммы на счете")
    creditDebitIndicator: str = Field(..., description="Индикатор типа операции (кредит или дебет)")
    type: str = Field(..., description="Тип баланса, например, 'текущий' или 'срочный'")


class CardResponse(BaseModel):
    accountId: str = Field(..., description="Уникальный идентификатор счета пользователя")
    balance: BalanceResponse = Field(..., description="Информация о балансе счета")
