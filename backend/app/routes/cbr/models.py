from fastapi import Query
from pydantic import BaseModel
from typing import List, Optional


class CbrParams:
    def __init__(
        self,
        rate_date: str = Query(default=None, description="информация по дате")
    ):
        self.rate_date = rate_date


class InflationGoal(BaseModel):
    id: int
    rate_value: float
    is_date: str


class InflationData(BaseModel):
    id: int
    rate_value: float
    is_date: str
    period: str


class KeyRate(BaseModel):
    id: int
    rate_value: float
    rate_change_date: str
    next_meeting_date: str
    is_date: str


class InterbankRate(BaseModel):
    id: int
    rate_name: str
    rate_today: str
    rate_tomorrow: Optional[str]
    is_date: str


class CurrencyRate(BaseModel):
    id: int
    currency_name: str
    rate_today: float
    rate_tomorrow: float
    is_date: str


class MetalPrice(BaseModel):
    id: int
    metal_name: str
    price_today: float
    price_tomorrow: float
    is_date: str


class Reserve(BaseModel):
    id: int
    reserve_value: Optional[float]
    rate_date: str
    is_date: str


class BankRequirement(BaseModel):
    id: int
    requirement_name: str
    rate_value: Optional[float]
    is_date: str


class ComplexCBR_Response(BaseModel):
    inflation_goal: List[InflationGoal]
    inflation_data: List[InflationData]
    key_rate: List[KeyRate]
    interbank_rate: List[InterbankRate]
    currency_rate: List[CurrencyRate]
    metal_price: List[MetalPrice]
    reserve: List[Reserve]
    liquidity_indicator: List[dict]
    bank_requirement: List[BankRequirement]
