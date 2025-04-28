from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scrapyrta.app.api import router as api_router
from scrapyrta.app.core.config import app_settings
from scrapyrta.app.core.log import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {app_settings.PROJECT_NAME} API")
    yield
    logger.info(f"Shutting down {app_settings.PROJECT_NAME} API")


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_settings.PROJECT_NAME,
        description="Asynchronous HTTP API for running Scrapy spiders",
        version="0.1.0",
        docs_url="/docs" if app_settings.ENABLE_OPEN_API else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["X-Requested-With"],
        allow_credentials=False,
    )

    app.include_router(api_router)

    return app
