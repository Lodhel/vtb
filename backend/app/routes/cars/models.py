from fastapi import Query


class CarParams:
    def __init__(
        self,
        model_car: str = Query(..., description="модель авто"),
        year: int = Query(..., description="год выпуска"),
        transmission_type: str = Query(..., description="тип КПП")
    ):
        self.model_car = model_car
        self.year = year
        self.transmission_type = transmission_type
