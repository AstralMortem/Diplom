from backend.config import config
from fastapi.responses import JSONResponse
from fastapi import status as status


class MedServiceException(Exception):
    def __init__(
        self,
        code: int,
        title: str,
        description: str | None = None,
        debug: str | Exception | None = None,
        headers: dict | None = None,
    ):
        self.code = code
        self.title = title
        self.description = description
        self.debug = debug
        self.headers = headers

    def to_response(self):
        response_content = {
            "code": self.code,
            "title": self.title,
            "description": self.description,
            "debug": str(self.debug) if config.DEBUG else None,
        }

        return JSONResponse(
            status_code=self.code, content=response_content, headers=self.headers
        )
