"""Decane SDK error types."""

from __future__ import annotations


class DecaneError(Exception):
    """Base error for all Decane SDK errors."""

    def __init__(self, message: str, code: str | None = None, status: int | None = None):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, code={self.code!r}, status={self.status})"


class AuthenticationError(DecaneError):
    """Invalid or missing API key."""

    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message, code="authentication_error", status=401)


class NotFoundError(DecaneError):
    """Resource not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="not_found", status=404)


class ValidationError(DecaneError):
    """Invalid request parameters."""

    def __init__(self, message: str = "Validation error", errors: list[dict] | None = None):
        self.errors = errors or []
        super().__init__(message, code="validation_error", status=422)


class RateLimitError(DecaneError):
    """Too many requests."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: float | None = None):
        self.retry_after = retry_after
        super().__init__(message, code="rate_limit", status=429)


class ServerError(DecaneError):
    """Server-side error."""

    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, code="server_error", status=500)


class InvalidSignatureError(DecaneError):
    """Webhook signature verification failed."""

    def __init__(self, message: str = "Invalid webhook signature"):
        super().__init__(message, code="invalid_signature", status=None)
