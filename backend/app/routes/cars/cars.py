from fastapi import APIRouter, Request, Response, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.cars.response_models import cars_responses
from backend.app.routes.general_models import GeneralHeadersModel

car_router = APIRouter()
car_tags = ["car_router"]


@cbv(car_router)
class CarRouter(ManagerSQLAlchemy):

    @car_router.get(
        "/auth/",
        name='auth_user',
        responses=cars_responses,
        description='Авторизация',
        tags=car_tags
    )
    async def get(self, request: Request, response: Response, headers: GeneralHeadersModel = Depends()):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            pass
