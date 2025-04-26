from typing import Optional, Dict
from pydantic import BaseModel
from fastapi import HTTPException as FastAPIHTTPException
from crypticorn.common import ApiError


class ExceptionDetail(BaseModel):
    message: str
    error: ApiError


class HTTPException(FastAPIHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: ExceptionDetail | str,
        headers: Optional[Dict[str, str]] = None,
    ):
        try:
            exc = (
                ExceptionDetail(**detail)
                if not isinstance(detail, ExceptionDetail)
                else detail
            )
        except Exception as e:
            exc = ExceptionDetail(
                message=detail,
                error=ApiError.UNKNOWN_ERROR,
            )

        super().__init__(
            status_code=status_code, detail=exc.model_dump(), headers=headers
        )
