# ══════════════════════════════════════════════════════════════
#  api/v1/market.py  —  Market Data Routes
#
#  Endpoints:
#    GET /api/v1/market/           → Get all market items
#    GET /api/v1/market/search?q=  → Search by name or symbol
#    GET /api/v1/market/{symbol}   → Get one item by symbol
#
#  These routes are PUBLIC — no token required.
#  Anyone can browse market data.
# ══════════════════════════════════════════════════════════════

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.market import MarketDataResponse
from app.services.market_service import MarketService


router = APIRouter()


@router.get(
    "/market/",
    response_model=List[MarketDataResponse],
    summary="Get all market data",
)
async def get_all_market_data(
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a list of all available market items (stocks, crypto, etc.).
    Sorted alphabetically by symbol.
    """
    return await MarketService.get_all_items(db)


@router.get(
    "/market/search",
    response_model=List[MarketDataResponse],
    summary="Search market data",
)
async def search_market_data(
    q: str = Query(..., min_length=1, description="Search keyword", example="Apple"),
    db: AsyncSession = Depends(get_db),
):
    """
    Search market items by name or symbol.
    
    - `?q=Apple` → matches "Apple Inc."
    - `?q=AAP`   → matches symbol "AAPL"
    - `?q=BTC`   → matches "Bitcoin" or symbol "BTC"
    """
    return await MarketService.search_items(q, db)


@router.get(
    "/market/{symbol}",
    response_model=MarketDataResponse,
    summary="Get market item by symbol",
)
async def get_market_item_by_symbol(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific market item by its ticker symbol.
    
    Examples:
    - `/market/AAPL`  → Apple Inc.
    - `/market/BTC`   → Bitcoin
    - `/market/GOOGL` → Alphabet Inc.
    """
    return await MarketService.get_by_symbol(symbol, db)
