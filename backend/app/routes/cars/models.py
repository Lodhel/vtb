from fastapi import Query
from pydantic import BaseModel, Field


class CarParams:
    def __init__(
        self,
        model_car: str = Query(None, description="Модель автомобиля, например, 'Toyota Camry'"),
        year: int = Query(None, description="Год выпуска автомобиля"),
        transmission_type: str = Query(None, description="Тип коробки передач, например, 'Автомат' или 'Механика'")
    ):
        self.model_car = model_car
        self.year = year
        self.transmission_type = transmission_type


class CarResponse(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор автомобиля")
    model_car: str = Field(..., description="Модель автомобиля")
    year: int = Field(..., description="Год выпуска автомобиля")
    transmission_type: str = Field(..., description="Тип коробки передач, например, 'Автомат' или 'Механика'")
    body_type: str = Field(..., description="Тип кузова, например, 'Седан' или 'Внедорожник'")
    fuel_type: str = Field(..., description="Тип топлива, например, 'Бензин' или 'Дизель'")
    average_price: int = Field(..., description="Средняя цена автомобиля в рублях")
    status: str = Field(..., description="Статус автомобиля, например, 'Новый' или 'С пробегом'")
