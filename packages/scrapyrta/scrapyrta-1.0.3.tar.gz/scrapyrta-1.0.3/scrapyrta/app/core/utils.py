from scrapy.settings import Settings
from scrapy.spiderloader import SpiderLoader
from scrapy.spiders import Spider

from scrapyrta.app.core.config import app_settings
from scrapyrta.app.core.exceptions import SpiderNotFoundError


def get_project_settings(
    module: str | None = None,
    custom_settings: dict | None = None,
) -> Settings:
    crawler_settings = Settings()

    if module is None:
        module = app_settings.PROJECT_SETTINGS

    if custom_settings is None:
        custom_settings = {}

    crawler_settings.setmodule(module, priority="project")

    if custom_settings:
        crawler_settings.setdict(custom_settings, priority="cmdline")

    return crawler_settings


def get_spider_class(spider_name: str) -> type[Spider]:
    try:
        spider_loader = SpiderLoader.from_settings(settings=get_project_settings())
        spider_class = spider_loader.load(spider_name)

        return spider_class

    except KeyError as e:
        raise SpiderNotFoundError(spider_name) from e
