from scrapy.settings import Settings

from scrapyrta.app.core.config import app_settings
from scrapyrta.app.core.utils import get_project_settings


def get_spider_settings(custom_settings: dict | None = None) -> Settings:
    if custom_settings is None:
        custom_settings = {}

    settings = get_project_settings()

    default_settings = {
        "DEBUG": app_settings.DEBUG,
        "LOG_ENABLED": app_settings.DEBUG,
        "LOG_LEVEL": app_settings.LOG_LEVEL,
        "TELNETCONSOLE_ENABLED": False,
        "EXTENSIONS": {
            "scrapy.webservice.WebService": None,
            "scrapy.extensions.logstats.LogStats": None,
            "scrapy.extensions.throttle.AutoThrottle": None,
        },
    }

    settings.update(default_settings, priority="project")
    settings.update(custom_settings, priority="spider")

    return settings
