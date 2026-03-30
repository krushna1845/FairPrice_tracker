# ══════════════════════════════════════════════════════════════
#  tests/test_auth.py  —  Auth API Tests
#
#  Tests for: register, login, wrong password
#
#  Run all tests:
#    pytest tests/ -v
#
#  Run just this file:
#    pytest tests/test_auth.py -v
# ══════════════════════════════════════════════════════════════

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_register_new_user():
    """A new user should be able to register and get a token."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/register", json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "securepassword123",
        })

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data        # Token must be returned
    assert data["email"] == "testuser@example.com"
    assert data["name"] == "Test User"


@pytest.mark.asyncio
async def test_login_existing_user():
    """A registered user should be able to login."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/login", json={
            "email": "testuser@example.com",
            "password": "securepassword123",
        })

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401():
    """Wrong password should return 401 Unauthorized."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/login", json={
            "email": "testuser@example.com",
            "password": "wrongpassword",
        })

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_400():
    """Registering with an email that already exists should return 400."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First registration
        await client.post("/api/v1/auth/register", json={
            "name": "User A",
            "email": "duplicate@example.com",
            "password": "password123",
        })
        # Second registration with same email
        response = await client.post("/api/v1/auth/register", json={
            "name": "User B",
            "email": "duplicate@example.com",
            "password": "password456",
        })

    assert response.status_code == 400
