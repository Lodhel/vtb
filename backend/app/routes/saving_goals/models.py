from fastapi import Query
from pydantic import BaseModel, Field


class GoalParams:
    def __init__(
        self,
        account_id: int = Query(
            None,
            description="Идентификатор накопительного счета, к которому привязана цель"
        )
    ):
        self.account_id = account_id


class GoalRequest(BaseModel):
    account_id: int = Field(..., description="ID накопительного счета, для которого создается цель")
    description: str = Field(..., description="Описание цели, например, 'накопить на отпуск'")
    target_amount: float = Field(..., description="Желаемая сумма, которую необходимо накопить для достижения цели")
    months_remaining: int = Field(..., description="Количество оставшихся месяцев для достижения цели")


class GoalResponse(BaseModel):
    description: str = Field(..., description="Описание цели")
    target_amount: float = Field(..., description="Желаемая сумма для накопления")
    recommended_contribution: float = Field(..., description="Рекомендуемая сумма вклада на следующий месяц")
    progress_percentage: float = Field(..., description="Процент выполнения цели на данный момент")
    rate_date: int = Field(..., description="Ожидаемая дата достижения цели")
