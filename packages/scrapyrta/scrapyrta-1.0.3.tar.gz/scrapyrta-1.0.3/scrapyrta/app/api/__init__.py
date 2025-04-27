from fastapi import APIRouter

from scrapyrta.app.api.v1 import router as v1_router
from scrapyrta.app.core.config import app_settings

router = APIRouter(prefix="")

router.include_router(v1_router)

if app_settings.DEBUG:

    @router.get("/")
    async def root():
        return {
            "message": f"Welcome to {app_settings.PROJECT_NAME} API",
            "docs": f"{router.prefix}/docs",
        }

    @router.get("/health")
    async def health_check():
        return {"status": "Healthy"}
