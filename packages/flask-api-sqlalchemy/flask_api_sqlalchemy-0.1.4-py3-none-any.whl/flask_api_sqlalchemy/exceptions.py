
# src/flask_api_sqlalchemy/exceptions.py
# Custom exceptions for the extension
class ApiError(Exception):
    """Base exception for API-related errors."""

    pass


class ModelDiscoveryError(ApiError):
    """Exception raised when model discovery fails."""

    pass


class ModelMappingError(ApiError):
    """Exception raised when model mapping fails."""

    pass
