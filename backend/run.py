from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware

from backend.app.routes import router
from backend.app.tasks.xg_boost_ml.calculate_deposit_manager import CalculateDepositManager


def create_app() -> FastAPI:
    app = FastAPI(
        title="MVP v.0.1",
        version="0.1.0",
        description="API MVP services.",
        docs_url=None,
        redoc_url="/openapi"
    )
    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    calculate_deposit_manager: CalculateDepositManager = CalculateDepositManager()

    @app.on_event("startup")
    @repeat_every(seconds=60)
    async def run_calculate_progress_percentage():
        await calculate_deposit_manager.run()
        return

    return app


application: FastAPI = create_app()
