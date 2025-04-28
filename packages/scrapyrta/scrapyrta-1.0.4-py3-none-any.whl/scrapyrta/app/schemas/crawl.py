from typing import Any

from pydantic import BaseModel, Field, field_validator


class SpiderSettings(BaseModel):
    url: str | None = None


class CrawlRequest(BaseModel):
    spider_name: str
    spider_config: SpiderSettings | None = None

    crawl_args: dict[str, Any] = Field(
        default=dict(),
        description="Additional arguments for the spider",
    )
    start_requests: bool = Field(
        default=False,
        description="Whether to use spider's start_requests method",
    )

    @field_validator("spider_config", mode="before")
    @classmethod
    def validate_request_or_start_requests(cls, v, info):
        if not v and not info.data.get("start_requests"):
            raise ValueError(
                "Either 'request.url' or 'start_requests' must be provided"
            )
        return v


class CrawlResponse(BaseModel):
    items: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    stats: dict[str, Any] = {}
