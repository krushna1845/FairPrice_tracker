# ══════════════════════════════════════════════════════════════
#  schemas/user.py  —  User Request & Response Shapes
# ══════════════════════════════════════════════════════════════

from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


class UserResponse(BaseModel):
    """
    User data returned in API responses.
    
    IMPORTANT: We NEVER include the password in responses.
    
    Example JSON:
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "John Doe",
        "email": "john@example.com",
        "role": "USER",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00"
    }
    """
    id: UUID
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        # This allows Pydantic to read data directly from SQLAlchemy model objects
        from_attributes = True


class UpdateUserRequest(BaseModel):
    """
    Body for PUT /api/v1/users/me  (update your own profile)
    All fields are optional — only send what you want to change.

    Example JSON:
    {
        "name": "Jane Doe"
    }
    """
    name: str | None = None    # Optional — only update if provided
    email: EmailStr | None = None
