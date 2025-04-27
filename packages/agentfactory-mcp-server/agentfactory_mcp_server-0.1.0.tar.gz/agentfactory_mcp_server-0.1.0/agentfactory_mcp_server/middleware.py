"""Middleware for error handling and request processing."""

import json
import logging
from typing import Any, Dict, Optional, Union

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ErrorResponse:
    """Standard error response format."""
    
    def __init__(
        self,
        error_code: str,
        detail: Optional[Union[str, Dict[str, Any]]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.error_code = error_code
        self.detail = detail
        self.status_code = status_code
    
    def to_response(self) -> JSONResponse:
        """Convert to FastAPI JSONResponse."""
        content = {"error_code": self.error_code}
        if self.detail:
            content["details"] = str(self.detail) if isinstance(self.detail, Exception) else self.detail
        return JSONResponse(status_code=self.status_code, content=content)


def register_error_handlers(app: FastAPI) -> None:
    """Register error handlers for the FastAPI application."""
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors from request parsing."""
        logger.warning(f"Validation error: {exc.errors()}")
        return ErrorResponse(
            error_code="E_SCHEMA",
            detail=exc.errors(),
            status_code=status.HTTP_400_BAD_REQUEST,
        ).to_response()
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        """Handle Pydantic validation errors."""
        logger.warning(f"Pydantic validation error: {exc.errors()}")
        return ErrorResponse(
            error_code="E_SCHEMA",
            detail=exc.errors(),
            status_code=status.HTTP_400_BAD_REQUEST,
        ).to_response()
        
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle ValueError exceptions."""
        logger.warning(f"ValueError: {str(exc)}")
        return ErrorResponse(
            error_code="E_PARAM",
            detail=str(exc),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ).to_response()
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            return ErrorResponse(
                error_code="E_NOT_FOUND",
                detail=exc.detail,
                status_code=exc.status_code,
            ).to_response()
        elif exc.status_code == status.HTTP_409_CONFLICT:
            return ErrorResponse(
                error_code="E_CATALOG",
                detail=exc.detail,
                status_code=exc.status_code,
            ).to_response()
        elif exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            return ErrorResponse(
                error_code="E_PARAM",
                detail=exc.detail,
                status_code=exc.status_code,
            ).to_response()
        elif exc.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            return ErrorResponse(
                error_code="E_CAPACITY",
                detail=exc.detail,
                status_code=exc.status_code,
            ).to_response()
        else:
            return ErrorResponse(
                error_code="E_UNKNOWN",
                detail=exc.detail,
                status_code=exc.status_code,
            ).to_response()
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle uncaught exceptions."""
        logger.exception(f"Uncaught exception: {str(exc)}")
        return ErrorResponse(
            error_code="E_INTERNAL",
            detail="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ).to_response()