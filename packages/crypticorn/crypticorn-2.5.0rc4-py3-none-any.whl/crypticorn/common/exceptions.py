from enum import Enum
from typing import Optional, Dict, Type
from pydantic import BaseModel, Field
from fastapi import HTTPException as FastAPIHTTPException, Request, FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from crypticorn.common import ApiError, ApiErrorIdentifier, ApiErrorType, ApiErrorLevel

class EnrichedDetail(BaseModel):
    '''This is the detail of the exception. It is used to enrich the exception with additional information by unwrapping the ApiError into its components.'''
    message: Optional[str] = Field(None, description="An additional error message")
    code: ApiErrorIdentifier = Field(..., description="The unique error code")
    type: ApiErrorType = Field(..., description="The type of error")
    level: ApiErrorLevel = Field(..., description="The level of the error")
    status_code: int = Field(..., description="The HTTP status code")


class ExceptionDetail(BaseModel):
    '''This is the detail of the exception. Pass an ApiError to the constructor and an optional human readable message.'''
    error: ApiError = Field(..., description="The unique error code")
    message: Optional[str] = Field(None, description="An additional error message")

    def enrich(self) -> EnrichedDetail:
        return EnrichedDetail(
            message=self.message,
            code=self.error.identifier,
            type=self.error.type,
            level=self.error.level,
            status_code=self.error.status_code,
        )

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
        assert isinstance(detail, ExceptionDetail)
        body = detail.enrich()
        super().__init__(
            status_code=body.status_code,
            detail=body.model_dump(mode="json"),
            headers=headers,
        )

async def general_handler(request: Request, exc: Exception):
    '''This is the default exception handler for all exceptions.'''
    body = ExceptionDetail(message=str(exc), error=ApiError.UNKNOWN_ERROR)
    return JSONResponse(status_code=body.error.status_code, content=HTTPException(detail=body).detail)

async def request_validation_handler(request: Request, exc: RequestValidationError):
    '''This is the exception handler for all request validation errors.'''
    body = ExceptionDetail(message=str(exc), error=ApiError.INVALID_DATA_REQUEST)
    return JSONResponse(status_code=body.error.status_code, content=HTTPException(detail=body).detail)

async def response_validation_handler(request: Request, exc: ResponseValidationError):
    '''This is the exception handler for all response validation errors.'''
    body = ExceptionDetail(message=str(exc), error=ApiError.INVALID_DATA_RESPONSE)
    return JSONResponse(status_code=body.error.status_code, content=HTTPException(detail=body).detail)

async def http_handler(request: Request, exc: HTTPException):
    '''This is the exception handler for HTTPExceptions. It unwraps the HTTPException and returns the detail in a flat JSON response.'''
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

def register_exception_handlers(app: FastAPI):
    '''Utility to register serveral exception handlers in one go. Catches Exception, HTTPException and Data Validation errors and responds with a unified json body.'''
    app.add_exception_handler(Exception, general_handler)
    app.add_exception_handler(FastAPIHTTPException, http_handler)
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(ResponseValidationError, response_validation_handler)

exception_response = {
    "default": {"model": EnrichedDetail, "description": "Error response"}
}