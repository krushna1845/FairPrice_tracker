# ══════════════════════════════════════════════════════════════
#  schemas/auth.py  —  Auth Request & Response Shapes
#
#  Pydantic schemas define the SHAPE of data coming in (requests)
#  and going out (responses) from your API.
#
#  FastAPI uses these to:
#    1. Validate incoming JSON automatically
#    2. Show correct examples in Swagger /docs
#    3. Return clean, predictable JSON responses
# ══════════════════════════════════════════════════════════════

from pydantic import BaseModel, Field


# ── Request Schemas (Data Coming IN) ───────────────────────────

class RegisterRequest(BaseModel):
    """
    Body expected when calling POST /api/v1/auth/register

    Example JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "mypassword123"
    }
    """
    name: str = Field(..., max_length=100, example="John Doe")
    email: str = Field(..., example="john@example.com")
    password: str = Field(..., example="mypassword123")


class LoginRequest(BaseModel):
    """
    Body expected when calling POST /api/v1/auth/login

    Example JSON:
    {
        "email": "john@example.com",
        "password": "mypassword123"
    }
    """
    email: str = Field(..., example="john@example.com")
    password: str = Field(..., example="mypassword123")


# ── Response Schemas (Data Going OUT) ──────────────────────────

class TokenResponse(BaseModel):
    """
    Response returned after successful register or login.

    Example JSON:
    {
        "access_token": "eyJhbGci...",
        "token_type": "bearer",
        "user_id": "abc-123",
        "name": "John Doe",
        "email": "john@example.com"
    }
    
    The frontend should store `access_token` and send it
    in all future requests as:  Authorization: Bearer <token>
    """
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str
