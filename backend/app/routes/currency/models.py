import datetime

from fastapi import Query
from pydantic import BaseModel
from typing import List


class CurrencyParams:
    def __init__(
        self,
        rate_date: str = Query(default=None, description="информация по дате"),
        currency_type: str = Query(default=None, description="какая валюта USD EUR CNY")
    ):
        self.rate_date = rate_date
        self.currency_type = currency_type


class CurrencyData(BaseModel):
    id: int
    is_date: datetime.date
    rate: float
    currency_type: str


class CurrencyResponse(BaseModel):
    data: List[CurrencyData]

    class Config:
        orm_mode = True
