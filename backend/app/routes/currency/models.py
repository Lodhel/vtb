import datetime
from fastapi import Query
from pydantic import BaseModel, Field
from typing import List


class CurrencyParams:
    def __init__(
        self,
        rate_date: str = Query(
            default=None,
            description="Дата, для которой требуется информация о курсе (в формате ГГГГ-ММ-ДД)"
        ),
        currency_type: str = Query(
            default=None,
            description="Тип валюты: USD, EUR, CNY"
        )
    ):
        self.rate_date = rate_date
        self.currency_type = currency_type


class CurrencyData(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор записи курса валюты")
    is_date: datetime.date = Field(..., description="Дата, на которую установлен курс валюты")
    rate: float = Field(..., description="Курс валюты на указанную дату")
    currency_type: str = Field(..., description="Тип валюты (например, USD, EUR, CNY)")


class CurrencyResponse(BaseModel):
    data: List[CurrencyData] = Field(..., description="Список данных по курсам валют")

    class Config:
        orm_mode = True
