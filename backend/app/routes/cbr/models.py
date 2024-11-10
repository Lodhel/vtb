import datetime
from fastapi import Query
from pydantic import BaseModel, Field
from typing import List, Optional, Any


class CbrParams:
    def __init__(
        self,
        rate_date: str = Query(
            default=None,
            description="Дата получения информации о курсе (в формате ГГГГ-ММ-ДД)"
        )
    ):
        self.rate_date = rate_date


class InflationParams:
    def __init__(
        self,
        rate_date: str = Query(
            default=None,
            description="Дата получения информации по инфляции (в формате ГГГГ-ММ-ДД)"
        )
    ):
        self.rate_date = rate_date


class InflationResponseData(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор записи инфляции")
    is_date: datetime.date = Field(..., description="Дата записи инфляции")
    rate: float = Field(..., description="Процент текущей ставки инфляции")
    inflation_rate: float = Field(..., description="Процент инфляции на указанную дату")


class InflationResponse(BaseModel):
    data: List[InflationResponseData] = Field(..., description="Список данных по инфляции")

    class Config:
        orm_mode = True


class InflationGoal(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор цели инфляции")
    rate_value: float = Field(..., description="Целевое значение инфляции")
    is_date: Any = Field(..., description="Дата целевого значения инфляции")


class InflationData(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор данных инфляции")
    rate_value: float = Field(..., description="Значение инфляции")
    is_date: Any = Field(..., description="Дата записи инфляции")
    period: str = Field(..., description="Период, к которому относится инфляция")


class KeyRate(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор ключевой ставки")
    rate_value: float = Field(..., description="Текущее значение ключевой ставки")
    rate_change_date: Any = Field(..., description="Дата изменения ставки")
    next_meeting_date: Any = Field(..., description="Дата следующего заседания")


class InterbankRate(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор межбанковской ставки")
    rate_name: str = Field(..., description="Название межбанковской ставки")
    rate_today: str = Field(..., description="Значение ставки на сегодня")
    rate_tomorrow: Optional[str] = Field(None, description="Значение ставки на завтра")
    is_date: Any = Field(..., description="Дата записи межбанковской ставки")


class CurrencyRate(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор валютного курса")
    currency_name: str = Field(..., description="Название валюты")
    rate_today: float = Field(..., description="Курс валюты на сегодня")
    rate_tomorrow: float = Field(..., description="Курс валюты на завтра")
    is_date: Any = Field(..., description="Дата записи курса")


class MetalPrice(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор цены металла")
    metal_name: str = Field(..., description="Название металла")
    price_today: float = Field(..., description="Цена металла на сегодня")
    price_tomorrow: float = Field(..., description="Цена металла на завтра")
    is_date: Any = Field(..., description="Дата записи цены")


class Reserve(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор резерва")
    reserve_value: Optional[float] = Field(None, description="Значение резерва")
    rate_date: str | datetime.date = Field(..., description="Дата записи резерва")
    is_date: Any = Field(..., description="Дата записи")


class BankRequirement(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор банковского требования")
    requirement_name: str = Field(..., description="Название банковского требования")
    rate_value: Optional[float] = Field(None, description="Значение банковского требования")
    is_date: Any = Field(..., description="Дата записи требования")


class ComplexCBR_Response(BaseModel):
    inflation_goal: List[InflationGoal] = Field(..., description="Список целевых показателей инфляции")
    inflation_data: List[InflationData] = Field(..., description="Список данных по инфляции")
    key_rate: List[KeyRate] = Field(..., description="Список данных по ключевой ставке")
    interbank_rate: List[InterbankRate] = Field(..., description="Список межбанковских ставок")
    currency_rate: List[CurrencyRate] = Field(..., description="Список валютных курсов")
    metal_price: List[MetalPrice] = Field(..., description="Список цен на металлы")
    reserve: List[Reserve] = Field(..., description="Список данных по резервам")
    liquidity_indicator: List[dict] = Field(..., description="Список индикаторов ликвидности")
    bank_requirement: List[BankRequirement] = Field(..., description="Список банковских требований")

    class Config:
        orm_mode = True
