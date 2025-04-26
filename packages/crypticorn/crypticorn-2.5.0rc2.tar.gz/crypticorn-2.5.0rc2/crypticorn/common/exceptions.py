from typing import Optional, Dict
from pydantic import BaseModel, Field
from fastapi import HTTPException as FastAPIHTTPException
from crypticorn.common import ApiError


class ExceptionDetail(BaseModel):
    message: Optional[str] = Field(None, description="An additional error message")
    error: ApiError = Field(..., description="The unique error code")


class HTTPException(FastAPIHTTPException):
    """A custom HTTP exception wrapper around FastAPI's HTTPException.
    It allows for a more structured way to handle errors, with a message and an error code. The status code is being derived from the detail's error.
        The ApiError class is the source of truth for everything. If the error is not yet implemented, there are fallbacks to avoid errors while testing.
    """

    def __init__(
        self,
        detail: ExceptionDetail,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            status_code=detail.error.status_code,
            detail=detail.model_dump(),
            headers=headers,
        )
