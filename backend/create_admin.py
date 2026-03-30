import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest

async def make_admin():
    async with AsyncSessionLocal() as db:
        try:
            req = RegisterRequest(
                name="Administrator",
                email="admin@admin.com",
                password="adminpassword"
            )
            token = await AuthService.register_user(req, db)
            print("Successfully created admin! Token:", token.access_token)
        except Exception as e:
            print("Error creating admin:", str(e))

if __name__ == "__main__":
    asyncio.run(make_admin())
