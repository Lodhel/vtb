from pydantic import BaseModel, Field


class UserProfileRequest(BaseModel):
    income_last_month: float = Field(..., description="Доход за последний месяц")
    expenses_last_month: float = Field(..., description="Расходы за последний месяц")
    savings_last_month: float = Field(..., description="Сумма, которую удалось отложить за последний месяц")
    marital_status: bool = Field(..., description="Семейное положение: True - женат/замужем, False - неженат/не замужем")
    children_count: int = Field(..., description="Количество детей")
    education: str = Field(..., description="Уровень образования: 'среднее', 'высшее' или 'послевузовское'")
    occupation: str = Field(..., description="Занятость: 'самозанятый', 'госслужащий', 'работник частной компании'")


class UserProfileResponse(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    income_last_month: float = Field(..., description="Доход за последний месяц")
    expenses_last_month: float = Field(..., description="Расходы за последний месяц")
    savings_last_month: float = Field(..., description="Сумма, которую удалось отложить за последний месяц")
    marital_status: bool = Field(..., description="Семейное положение: True - женат/замужем, False - неженат/не замужем")
    children_count: int = Field(..., description="Количество детей")
    education: str = Field(..., description="Уровень образования: 'среднее', 'высшее' или 'послевузовское'")
    occupation: str = Field(..., description="Занятость: 'самозанятый', 'госслужащий', 'работник частной компании'")

    class Config:
        orm_mode = True
