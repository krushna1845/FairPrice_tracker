# ══════════════════════════════════════════════════════════════
#  core/dependencies.py  —  Shared Route Dependencies
#
#  A "dependency" in FastAPI is a function that runs BEFORE
#  your route handler. Think of it as middleware per-route.
#
#  `get_current_user` is the most important one:
#    - It reads the JWT token from the request header
#    - Decodes it to find the user ID
#    - Loads the user from the database
#    - Returns the User object to your route
#
#  Usage in any protected route:
#    async def my_route(current_user: User = Depends(get_current_user)):
#        print(current_user.name)  # ✅ you know who's logged in
# ══════════════════════════════════════════════════════════════

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User


# Tells FastAPI: "Look for the token at POST /api/v1/auth/login"
# It also makes the lock icon appear in Swagger UI (/docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Protected route dependency.
    
    Flow:
      1. Client sends request with header:  Authorization: Bearer <token>
      2. FastAPI extracts the token
      3. We decode it to get the user_id
      4. We load the User from the database
      5. We return the User to the route handler
    
    If anything goes wrong → raises 401 Unauthorized error.
    """

    # Standard error for any auth failure
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Step 1: Decode the token
    payload = decode_access_token(token)
    if payload is None:
        raise unauthorized  # Token is invalid or expired

    # Step 2: Extract user ID from the token payload
    user_id: str = payload.get("sub")
    if user_id is None:
        raise unauthorized  # Token doesn't contain a user ID

    # Step 3: Find the user in the database
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise unauthorized  # User was deleted after token was issued

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated.",
        )

    return user  # ✅ Route handler receives this User object
