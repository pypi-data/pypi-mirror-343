from asyncio import wait_for

from crochet import setup as setup_crochet
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.defer import deferred_to_future
from scrapy.utils.log import configure_logging

from scrapyrta.app.core.config import app_settings
from scrapyrta.app.core.config.spider_settings import get_spider_settings
from scrapyrta.app.core.exceptions import (
    SpiderRunError,
)
from scrapyrta.app.core.log import logger
from scrapyrta.app.core.utils import get_spider_class
from scrapyrta.app.schemas.crawl import CrawlRequest, CrawlResponse

setup_crochet()


async def run_spider(crawl_request: CrawlRequest) -> CrawlResponse:
    try:
        spider_cls = get_spider_class(crawl_request.spider_name)

        spider_kwargs = {}
        if not crawl_request.start_requests:
            if not crawl_request.spider_config or not crawl_request.spider_config.url:
                raise ValueError("URL is required when start_requests is False")

            spider_kwargs = crawl_request.spider_config.model_dump(exclude_none=True)
            spider_kwargs["start_urls"] = [crawl_request.spider_config.url]

        spider_kwargs.update(crawl_request.crawl_args)  # type: ignore

        results, errors = [], []

        def handle_item(item, response, spider):
            if item:
                results.append(item)

        def handle_event(failure, **kwargs):
            if failure:
                errors.append({"failure": failure.getErrorMessage()})

        dispatcher.connect(handle_item, signal=signals.item_passed)
        dispatcher.connect(handle_event, signal=signals.item_error)
        dispatcher.connect(handle_event, signal=signals.spider_error)

        runner_settings = get_spider_settings()

        configure_logging(settings=runner_settings)
        runner = CrawlerRunner(settings=runner_settings)
        deferred = runner.crawl(spider_cls, **spider_kwargs)

        crawler = next(iter(runner.crawlers))

        await wait_for(
            deferred_to_future(deferred),
            timeout=app_settings.TIMEOUT_LIMIT,
        )

        return CrawlResponse(
            items=results,
            errors=errors,
            stats=crawler.stats.get_stats(),
        )

    except TimeoutError as e:
        err_txt = "TimeoutError: The spider took too long to respond."
        logger.error(err_txt)

        raise SpiderRunError(crawl_request.spider_name, err_txt) from e

    except Exception as e:
        err_txt = f"{type(e).__name__}: {e}" if str(e) else f"{type(e).__name__}."
        logger.error(err_txt)

        raise SpiderRunError(crawl_request.spider_name) from e
