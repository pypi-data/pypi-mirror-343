from fastapi import APIRouter, HTTPException

from scrapyrta.app.core.exceptions import SpiderNotFoundError, SpiderRunError
from scrapyrta.app.schemas.crawl import CrawlRequest, CrawlResponse
from scrapyrta.app.services import run_spider

router = APIRouter(prefix="")


@router.post("/crawl.json", response_model=CrawlResponse)
async def start_crawl(request: CrawlRequest) -> CrawlResponse:
    """
    Start a spider crawl with the specified parameters.

    The spider can be started in two ways:
    1. By providing a URL in the request
    2. By enabling start_requests
    """

    exception_handlers = {
        SpiderNotFoundError: 404,
        SpiderRunError: 500,
    }

    try:
        return await run_spider(crawl_request=request)

    except tuple(exception_handlers.keys()) as e:
        status_code = exception_handlers[type(e)]
        raise HTTPException(status_code=status_code, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {e!s}",
        ) from e
