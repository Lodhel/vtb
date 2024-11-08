from fastapi import Query
from pydantic import BaseModel


class CarParams:
    def __init__(
        self,
        model_car: str = Query(None, description="модель авто"),
        year: int = Query(None, description="год выпуска"),
        transmission_type: str = Query(None, description="тип КПП")
    ):
        self.model_car = model_car
        self.year = year
        self.transmission_type = transmission_type


class CarResponse(BaseModel):
    id: int
    model_car: str
    year: int
    transmission_type: str
    body_type: str
    fuel_type: str
    average_price: int
    status: str
