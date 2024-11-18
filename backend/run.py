from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware

from backend.app.routes import router
from backend.app.tasks.calculate_progress_percentage import CalculateManager


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

    calculate_progress_percentage_manager = CalculateManager()

    @app.on_event("startup")
    @repeat_every(seconds=60)
    async def run_calculate_progress_percentage():
        await calculate_progress_percentage_manager.run()
        return

    return app


application: FastAPI = create_app()
