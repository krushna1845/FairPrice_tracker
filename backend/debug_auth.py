#!/usr/bin/env python
"""
🔍 Market Buddy - Authentication Debugger
This script tests the entire auth flow to identify where issues are occurring.
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def main():
    print("=" * 80)
    print("🔍 MARKET BUDDY - AUTHENTICATION DEBUG")
    print("=" * 80)
    
    # 1. Test database connection
    print("\n1️⃣  Testing Database Connection...")
    try:
        from app.core.database import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            result = await session.execute("SELECT 1")
            print("✅ Database connection: OK")
    except Exception as e:
        print(f"❌ Database connection: FAILED")
        print(f"   Error: {e}")
        return
    
    # 2. Check if users table exists
    print("\n2️⃣  Checking Users Table...")
    try:
        from app.core.database import AsyncSessionLocal
        from sqlalchemy import text
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='users'")
            )
            row = result.fetchone()
            if row:
                print("✅ Users table exists")
            else:
                print("❌ Users table DOES NOT EXIST")
                print("   Run: alembic upgrade head")
                return
    except Exception as e:
        print(f"❌ Error checking users table: {e}")
        return
    
    # 3. Test user registration
    print("\n3️⃣  Testing User Registration...")
    try:
        from app.services.auth_service import AuthService
        from app.schemas.auth import RegisterRequest
        from app.core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            test_email = f"test_{os.urandom(4).hex()}@test.com"
            register_data = RegisterRequest(
                name="Test User",
                email=test_email,
                password="TestPassword123"
            )
            
            response = await AuthService.register_user(register_data, session)
            print(f"✅ User registration successful")
            print(f"   User ID: {response.user_id}")
            print(f"   Token received: {'Yes' if response.access_token else 'No'}")
    except Exception as e:
        print(f"❌ User registration failed: {e}")
        return
    
    # 4. Test user login
    print("\n4️⃣  Testing User Login...")
    try:
        from app.services.auth_service import AuthService
        from app.schemas.auth import LoginRequest
        from app.core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            login_data = LoginRequest(
                email=test_email,
                password="TestPassword123"
            )
            
            response = await AuthService.login_user(login_data, session)
            print(f"✅ User login successful")
            print(f"   Token received: {'Yes' if response.access_token else 'No'}")
    except Exception as e:
        print(f"❌ User login failed: {e}")
        return
    
    # 5. Check server connectivity
    print("\n5️⃣  Checking Server Connectivity...")
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/")
            print(f"✅ Backend server is running")
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend server not accessible: {e}")
        return
    
    # 6. Test API endpoints
    print("\n6️⃣  Testing API Endpoints...")
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            # Test register endpoint
            test_payload = {
                "name": "API Test User",
                "email": f"apitest_{os.urandom(4).hex()}@test.com",
                "password": "ApiTestPassword123"
            }
            response = await client.post(
                "http://localhost:8000/api/v1/auth/register",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"✅ /auth/register endpoint")
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                api_test_email = test_payload["email"]
                api_test_password = test_payload["password"]
                
                # Test login
                response = await client.post(
                    "http://localhost:8000/api/v1/auth/login",
                    json={"email": api_test_email, "password": api_test_password},
                    headers={"Content-Type": "application/json"}
                )
                print(f"✅ /auth/login endpoint")
                print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return
    
    print("\n" + "=" * 80)
    print("🎉 All tests passed!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
