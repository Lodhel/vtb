from fastapi import APIRouter, Request, Response, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import CarModel
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.cars.models import CarParams
from backend.app.routes.cars.response_models import cars_responses
from backend.app.routes.main import MainRouterMIXIN

car_router = APIRouter()
car_tags = ["car_router"]


@cbv(car_router)
class CarRouter(MainRouterMIXIN, ManagerSQLAlchemy):

    @car_router.get(
        "/auth/",
        name='auth_user',
        responses=cars_responses,
        description='Получение списка автомобилей',
        tags=car_tags
    )
    async def get(self, request: Request, response: Response, params: CarParams = Depends()):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions:
                car_models_select = await session.execute(select(CarModel).filter(conditions))
            else:
                car_models_select = await session.execute(select(CarModel))
            car_models = car_models_select.scalars().all()
            data: list = [
                self._get_data_by_response_created(car_model) for car_model in car_models
            ]
            result = self.get_data(data)
            return result

    @staticmethod
    def make_conditions(params: CarParams):
        conditions: list = []

        if params.model_car:
            conditions.append(CarModel.model_car == params.model_car)

        if params.year:
            conditions.append(CarModel.year == params.year)

        if params.transmission_type:
            conditions.append(CarModel.transmission_type == params.transmission_type)

        return and_(*conditions) if conditions else None

    @staticmethod
    def _get_data_by_response_created(car_model: CarModel) -> dict:
        return {
            'id': car_model.id,
            'model_car': car_model.model_car,
            'year': car_model.year,
            'transmission_type': car_model.transmission_type,
            'body_type': car_model.body_type,
            'fuel_type': car_model.fuel_type,
            'average_price': car_model.average_price,
            'status': car_model.status
        }
