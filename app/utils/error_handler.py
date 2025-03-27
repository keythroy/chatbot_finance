from fastapi import status
from . import logger
from fastapi.responses import JSONResponse
# from pydantic import ValidationError
# from sqlalchemy.exc import SQLAlchemyError


class CustomError(Exception):
    """
    Custom exception for application-specific errors.
    """
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

async def custom_error_handler(e):
    """
    Handler for custom exceptions.
    """
    logger.error(f"Custom error: {e.message}")
    return JSONResponse(
        status_code=e.status_code,
        content={"error": e.message},
    )

# async def http_error_handler(request: Request, exc: HTTPException):
#     """
#     Handler for HTTP exceptions (FastAPI).
#     """
#     logger.error(f"HTTP error: {exc.detail}")
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"error": exc.detail},
#     )

# async def validation_error_handler(request: Request, exc: ValidationError):
#     """
#     Handler for validation errors (Pydantic).
#     """
#     errors = exc.errors()
#     logger.error(f"Validation error: {errors}")
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"error": "Validation error", "details": errors},
#     )

# async def database_error_handler(request: Request, exc: SQLAlchemyError):
#     """
#     Handler for database errors (SQLAlchemy).
#     """
#     logger.error(f"Database error: {str(exc)}")
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={"error": "Database error", "details": str(exc)},
#     )

# async def generic_error_handler(request: Request, exc: Exception):
#     """
#     Handler for generic unhandled errors.
#     """
#     logger.error(f"Unexpected error: {str(exc)}")
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={"error": "Internal server error", "details": str(exc)},
#     )

# # Error handlers configuration
# error_handlers = {
#     # CustomError: custom_error_handler,
#     HTTPException: http_error_handler,
#     ValidationError: validation_error_handler,
#     SQLAlchemyError: database_error_handler,
#     Exception: generic_error_handler,
# }