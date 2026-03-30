# ══════════════════════════════════════════════════════════════
#  services/auth_service.py  —  Auth Business Logic
#
#  Services contain the BUSINESS LOGIC — the actual work.
#  Routes just call services; they don't contain logic themselves.
#
#  This keeps code organized:
#    Route   → "Who is calling and with what data?"
#    Service → "What should we actually DO with that data?"
# ══════════════════════════════════════════════════════════════

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    """Handles all authentication logic: register and login."""

    @staticmethod
    async def register_user(data: RegisterRequest, db: AsyncSession) -> TokenResponse:
        """
        Creates a new user account.

        Steps:
          1. Check if email is already registered
          2. Hash the password
          3. Save new user to the database
          4. Generate and return a JWT token
        """

        # Step 1: Make sure email is not already taken
        result = await db.execute(
            select(User).where(User.email == data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered. Please login instead.",
            )

        # Step 2 & 3: Create and save the new user
        new_user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password),  # NEVER store plain password
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)  # Reload to get the generated id and created_at

        # Step 4: Generate JWT token
        # "sub" (subject) = the user's unique ID — stored inside the token
        token = create_access_token({"sub": str(new_user.id)})

        return TokenResponse(
            access_token=token,
            user_id=str(new_user.id),
            name=new_user.name,
            email=new_user.email,
        )

    @staticmethod
    async def login_user(data: LoginRequest, db: AsyncSession) -> TokenResponse:
        """
        Logs in an existing user.

        Steps:
          1. Find user by email
          2. Verify the password matches the stored hash
          3. Generate and return a JWT token
        """

        # Step 1: Find user by email
        result = await db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        # Step 2: Verify password (use generic error — don't reveal if email exists)
        if user is None or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been deactivated.",
            )

        # Step 3: Generate JWT token
        token = create_access_token({"sub": str(user.id)})

        return TokenResponse(
            access_token=token,
            user_id=str(user.id),
            name=user.name,
            email=user.email,
        )
