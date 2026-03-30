# ══════════════════════════════════════════════════════════════
#  api/v1/auth.py  —  Authentication Routes
#
#  Endpoints:
#    POST /api/v1/auth/register  → Create a new account
#    POST /api/v1/auth/login     → Login and get a JWT token
#
#  These routes are PUBLIC — no token required.
# ══════════════════════════════════════════════════════════════

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import AuthService


# Create a router — a group of related endpoints
router = APIRouter()


@router.post(
    "/auth/register",
    response_model=TokenResponse,
    summary="Register a new user account",
    status_code=201,
)
async def register(
    data: RegisterRequest,          # FastAPI reads this from the request body (JSON)
    db: AsyncSession = Depends(get_db),  # Auto-inject database session
):
    """
    Creates a new user account and returns a JWT token.
    
    - **name**: Your full name (min 2 characters)
    - **email**: Must be unique — used to login
    - **password**: Min 6 characters (stored as a secure hash)
    
    After registering, use the `access_token` to make authenticated requests.
    """
    return await AuthService.register_user(data, db)


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Login with email and password",
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Logs in with email + password.
    
    Returns a JWT `access_token`. Include it in all protected requests:
    ```
    Authorization: Bearer <your_token_here>
    ```
    """
    return await AuthService.login_user(data, db)
