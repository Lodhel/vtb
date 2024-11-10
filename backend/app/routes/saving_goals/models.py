from pydantic import BaseModel


class GoalRequest(BaseModel):
    description: str
    target_amount: float
    months_remaining: int


class GoalResponse(BaseModel):
    description: str
    target_amount: float
    recommended_contribution: float
    progress_percentage: float
