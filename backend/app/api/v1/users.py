# ══════════════════════════════════════════════════════════════
#  api/v1/users.py  —  User Profile Routes
#
#  Endpoints:
#    GET /api/v1/users/me   → Get your own profile
#    PUT /api/v1/users/me   → Update your name or email
#
#  These routes are PROTECTED — a valid JWT token is required.
#  `Depends(get_current_user)` handles token validation automatically.
# ══════════════════════════════════════════════════════════════

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UpdateUserRequest


router = APIRouter()


@router.get(
    "/users/me",
    response_model=UserResponse,
    summary="Get my profile",
)
async def get_my_profile(
    # get_current_user reads the JWT token and returns the logged-in User
    current_user: User = Depends(get_current_user),
):
    """
    Returns the profile of the currently logged-in user.
    
    Requires: `Authorization: Bearer <token>` header.
    """
    return current_user  # Just return the user — no extra work needed


@router.put(
    "/users/me",
    response_model=UserResponse,
    summary="Update my profile",
)
async def update_my_profile(
    data: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Updates the logged-in user's name or email.
    Only include the fields you want to change.
    
    Example body:
    ```json
    { "name": "New Name" }
    ```
    """

    # Only update fields that were actually provided
    if data.name is not None:
        current_user.name = data.name

    if data.email is not None:
        current_user.email = data.email

    # Save changes to the database
    await db.commit()
    await db.refresh(current_user)

    return current_user
