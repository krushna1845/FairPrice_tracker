import asyncio
from app.core.database import AsyncSessionLocal
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService

async def run_test():
    try:
        async with AsyncSessionLocal() as db:
            req = RegisterRequest(name='test_user123', email='test1234567@test.com', password='password123')
            result = await AuthService.register_user(req, db)
            print("SUCCESS! Token:", result.access_token)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
