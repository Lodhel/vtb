from fastapi import Query
from pydantic import BaseModel, Field
from typing import Optional


class RecommendedDepositParams:
    def __init__(
        self,
        rate_date: Optional[str] = Query(None, description="Дата в формате 'YYYY-MM'")
    ):
        self.rate_date = rate_date


class RecommendedDepositResponse(BaseModel):
    recommended_deposit: float = Field(..., description="Рекомендуемая сумма депозита")
    rate_date: str = Field(..., description="Дата в формате 'год-месяц'")
