# ══════════════════════════════════════════════════════════════
#  tests/test_market.py  —  Market & Watchlist API Tests
# ══════════════════════════════════════════════════════════════

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_all_market_data_is_public():
    """Market listing should be accessible without a token."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/market/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_search_market_data():
    """Searching market data should return a list."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/market/search?q=Apple")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_nonexistent_symbol_returns_404():
    """Getting a symbol that doesn't exist should return 404."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/market/FAKESYMBOL999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_watchlist_requires_token():
    """Watchlist endpoint should reject requests without a token."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/watchlist/")

    assert response.status_code == 401  # Unauthorized


@pytest.mark.asyncio
async def test_dashboard_requires_token():
    """Dashboard endpoint should reject requests without a token."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/dashboard/summary")

    assert response.status_code == 401
