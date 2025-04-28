# ScrapyRTA

[![PyPI Downloads](https://static.pepy.tech/badge/scrapyrta)](https://pepy.tech/projects/scrapyrta)

ScrapyRTA is an asynchronous HTTP API for running Scrapy spiders, built with FastAPI. It's a modern rewrite of the legacy [ScrapyRT](https://github.com/scrapinghub/scrapyrt) project, focusing on asynchronous operation and scalability.

## Features

-   Run Scrapy spiders via an Async HTTP API
-   Configurable request parameters

### API Endpoints

#### POST /crawl.json

Run a spider with specified parameters.

Example request:

```bash
curl --data '{"request": {"url": "http://quotes.toscrape.com/page/2/"}, "spider_name": "toscrape-css", "crawl_args": {"zipcode":"14000"}}' http://localhost:9080/crawl -v
```

> Have a look at `http://127.0.0.1:9080/docs` for more details and examples.

You can also create an `.env` file with the following content to alter ScrapyRTA behavior:

```text
SCRAPYRTA_DEBUG=False
SCRAPYRTA_LOG_LEVEL=INFO
SCRAPYRTA_ENABLE_OPEN_API=False

SCRAPYRTA_TIMEOUT_LIMIT=30 # seconds
```

## Notes

-   Requires `scrapy.cfg` in project directory, raises error if missing.
