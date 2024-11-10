from fastapi import Query
from pydantic import BaseModel


class GoalParams:
    def __init__(
        self,
        account_id: int = Query(None, description="id накопительного счета")
    ):
        self.account_id = account_id


class GoalRequest(BaseModel):
    account_id: int
    description: str
    target_amount: float
    months_remaining: int


class GoalResponse(BaseModel):
    description: str
    target_amount: float
    recommended_contribution: float
    progress_percentage: float
