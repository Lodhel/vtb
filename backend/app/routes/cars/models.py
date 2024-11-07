from fastapi import Query

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
