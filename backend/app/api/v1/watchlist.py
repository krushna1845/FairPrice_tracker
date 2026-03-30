# ══════════════════════════════════════════════════════════════
#  api/v1/watchlist.py  —  Watchlist Routes
#
#  Endpoints:
#    GET    /api/v1/watchlist/          → Get my watchlist
#    POST   /api/v1/watchlist/          → Add item to watchlist
#    DELETE /api/v1/watchlist/{item_id} → Remove item from watchlist
#
#  All routes are PROTECTED — JWT token required.
#  Each user only sees and manages THEIR OWN watchlist.
# ══════════════════════════════════════════════════════════════

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.market import AddToWatchlistRequest, WatchlistItemResponse
from app.services.market_service import WatchlistService


router = APIRouter()


@router.get(
    "/watchlist/",
    response_model=List[WatchlistItemResponse],
    summary="Get my watchlist",
)
async def get_my_watchlist(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns all market items saved in the logged-in user's watchlist.
    Sorted by most recently added first.
    """
    return await WatchlistService.get_user_watchlist(str(current_user.id), db)


@router.post(
    "/watchlist/",
    summary="Add item to watchlist",
    status_code=201,
)
async def add_to_my_watchlist(
    data: AddToWatchlistRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Adds a market item to the logged-in user's watchlist.
    
    Body:
    ```json
    { "market_data_id": "uuid-of-the-market-item" }
    ```
    
    Returns 400 if the item is already in the watchlist.
    """
    return await WatchlistService.add_to_watchlist(str(current_user.id), data, db)


@router.delete(
    "/watchlist/{item_id}",
    summary="Remove item from watchlist",
)
async def remove_from_my_watchlist(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Removes a watchlist entry by its ID.
    Only the owner of the watchlist item can delete it.
    
    Returns 404 if the item doesn't exist or doesn't belong to you.
    """
    return await WatchlistService.remove_from_watchlist(str(current_user.id), item_id, db)
