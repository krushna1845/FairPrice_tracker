# ══════════════════════════════════════════════════════════════
#  utils/exceptions.py  —  Custom HTTP Exceptions
#
#  Shorthand exception classes for common HTTP errors.
#  Instead of writing the full HTTPException every time,
#  you can just raise NotFoundError("User not found").
# ══════════════════════════════════════════════════════════════

from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    """Raise when a resource doesn't exist. Returns HTTP 404."""
    def __init__(self, detail: str = "Resource not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedError(HTTPException):
    """Raise when user is not authenticated. Returns HTTP 401."""
    def __init__(self, detail: str = "Authentication required."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenError(HTTPException):
    """Raise when user doesn't have permission. Returns HTTP 403."""
    def __init__(self, detail: str = "You don't have permission to do this."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestError(HTTPException):
    """Raise when the request data is invalid. Returns HTTP 400."""
    def __init__(self, detail: str = "Invalid request."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ConflictError(HTTPException):
    """Raise when there's a data conflict (e.g. duplicate email). Returns HTTP 409."""
    def __init__(self, detail: str = "A conflict occurred."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
