# ══════════════════════════════════════════════════════════════
#  services/market_service.py  —  Market & Watchlist Business Logic
# ══════════════════════════════════════════════════════════════

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.market_data import MarketData
from app.models.watchlist import Watchlist
from app.schemas.market import AddToWatchlistRequest


class MarketService:
    """Handles fetching and searching market data."""

    @staticmethod
    async def get_all_items(db: AsyncSession) -> list[MarketData]:
        """
        Fetches all market items, sorted alphabetically by symbol.
        
        Returns: List of MarketData objects
        """
        result = await db.execute(
            select(MarketData).order_by(MarketData.symbol)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_symbol(symbol: str, db: AsyncSession) -> MarketData:
        """
        Fetches a single market item by its ticker symbol.
        
        Example: get_by_symbol("AAPL") → returns Apple's data
        Raises 404 if symbol doesn't exist.
        """
        result = await db.execute(
            select(MarketData).where(MarketData.symbol == symbol.upper())
        )
        item = result.scalar_one_or_none()

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Symbol '{symbol.upper()}' not found.",
            )

        return item

    @staticmethod
    async def search_items(query: str, db: AsyncSession) -> list[MarketData]:
        """
        Searches market items by name OR symbol.
        Case-insensitive search using SQL ILIKE.
        
        Example: search("app") matches "Apple", "AAPL"
        """
        search_pattern = f"%{query}%"  # SQL wildcard: matches anything containing the query

        result = await db.execute(
            select(MarketData).where(
                MarketData.name.ilike(search_pattern) |    # Match in name
                MarketData.symbol.ilike(search_pattern)    # OR match in symbol
            ).order_by(MarketData.symbol)
        )
        return result.scalars().all()


class WatchlistService:
    """Handles a user's personal watchlist."""

    @staticmethod
    async def get_user_watchlist(user_id: str, db: AsyncSession) -> list[Watchlist]:
        """
        Returns all watchlist items for a specific user.
        Includes the full market data for each item.
        """
        result = await db.execute(
            select(Watchlist)
            .where(Watchlist.user_id == user_id)
            .order_by(Watchlist.added_at.desc())  # Newest first
        )
        return result.scalars().all()

    @staticmethod
    async def add_to_watchlist(
        user_id: str,
        data: AddToWatchlistRequest,
        db: AsyncSession,
    ) -> Watchlist:
        """
        Adds a market item to the user's watchlist.
        Raises 400 if the item is already in their watchlist.
        """

        # Check if already in watchlist
        result = await db.execute(
            select(Watchlist).where(
                Watchlist.user_id == user_id,
                Watchlist.market_data_id == data.market_data_id,
            )
        )
        already_exists = result.scalar_one_or_none()

        if already_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This item is already in your watchlist.",
            )

        # Add new watchlist entry
        new_entry = Watchlist(
            user_id=user_id,
            market_data_id=data.market_data_id,
        )
        db.add(new_entry)
        await db.commit()
        await db.refresh(new_entry)

        return new_entry

    @staticmethod
    async def remove_from_watchlist(
        user_id: str,
        item_id: str,
        db: AsyncSession,
    ) -> dict:
        """
        Removes an item from the user's watchlist.
        Only deletes it if it belongs to THIS user (security check).
        """
        result = await db.execute(
            select(Watchlist).where(
                Watchlist.id == item_id,
                Watchlist.user_id == user_id,  # Important: only allow deletion of OWN items
            )
        )
        entry = result.scalar_one_or_none()

        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Watchlist item not found.",
            )

        await db.delete(entry)
        await db.commit()

        return {"message": "Item removed from watchlist successfully."}
