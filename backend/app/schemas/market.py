# ══════════════════════════════════════════════════════════════
#  schemas/market.py  —  Market & Watchlist Request/Response Shapes
# ══════════════════════════════════════════════════════════════

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class MarketDataResponse(BaseModel):
    """
    Market item data returned in API responses.

    Example JSON:
    {
        "id": "550e8400-...",
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": "189.3000",
        "change_percent": "1.2500",
        "volume": 55000000,
        "last_updated": "2024-01-15T10:30:00"
    }
    """
    id: UUID
    symbol: str
    name: str | None
    price: Decimal | None
    change_percent: Decimal | None
    volume: int | None
    market_cap: Decimal | None
    last_updated: datetime | None | None

    class Config:
        from_attributes = True  # Read from SQLAlchemy model


class AddToWatchlistRequest(BaseModel):
    """
    Body for POST /api/v1/watchlist/  (add item to watchlist)

    Example JSON:
    {
        "market_data_id": "550e8400-e29b-41d4-a716-446655440000"
    }
    """
    market_data_id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")


class WatchlistItemResponse(BaseModel):
    """
    Watchlist entry returned in API responses.
    Includes the full market data for the watched item.

    Example JSON:
    {
        "id": "abc-123",
        "added_at": "2024-01-15T10:30:00",
        "market_data": {
            "symbol": "AAPL",
            "price": "189.30",
            ...
        }
    }
    """
    id: UUID
    added_at: datetime
    market_data: MarketDataResponse

    class Config:
        from_attributes = True
