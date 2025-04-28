from fastapi import APIRouter

from scrapyrta.app.api.v1.crawls import router as crawls_router

router = APIRouter(prefix="")

router.include_router(crawls_router)
