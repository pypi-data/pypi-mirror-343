from fastapi import HTTPException


class ScrapyRTAException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SpiderNotFoundError(ScrapyRTAException):
    def __init__(self, spider_name: str):
        self.spider_name = spider_name
        message = f"Spider '{spider_name}' not found"
        super().__init__(message)


class SpiderRunError(ScrapyRTAException):
    def __init__(self, spider_name: str, message: str | None = None):
        self.spider_name = spider_name

        if message is None:
            message = f"Error running spider '{spider_name}': check logs for details."
        else:
            message = f"Error running spider '{spider_name}': {message}"

        super().__init__(message)


def spider_exception_handler(exception: ScrapyRTAException) -> HTTPException:
    status_code_map: dict[type[ScrapyRTAException], int] = {
        SpiderNotFoundError: 404,
        SpiderRunError: 500,
    }

    status_code = status_code_map.get(type(exception), 500)
    detail = (
        exception.message
        if isinstance(exception, ScrapyRTAException)
        else str(exception)
    )

    return HTTPException(status_code=status_code, detail=detail)
