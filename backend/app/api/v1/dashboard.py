# ══════════════════════════════════════════════════════════════
#  api/v1/dashboard.py  —  Dashboard Summary Route
#
#  Endpoint:
#    GET /api/v1/dashboard/summary → Summary stats for the user
#
#  Protected — JWT token required.
#  Returns a quick overview for the user's dashboard page.
# ══════════════════════════════════════════════════════════════

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.market_data import MarketData
from app.models.watchlist import Watchlist


router = APIRouter()


@router.get(
    "/dashboard/summary",
    summary="Get dashboard summary",
)
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a summary of stats for the logged-in user's dashboard.
    
    Response:
    ```json
    {
        "user": {
            "name": "John Doe",
            "email": "john@example.com",
            "member_since": "2024-01-15T10:30:00"
        },
        "stats": {
            "total_market_items": 100,
            "my_watchlist_count": 5
        }
    }
    ```
    """

    # Count all items available in the market
    market_count_result = await db.execute(
        select(func.count(MarketData.id))
    )
    total_market_items = market_count_result.scalar()

    # Count only THIS user's watchlist items
    watchlist_count_result = await db.execute(
        select(func.count(Watchlist.id))
        .where(Watchlist.user_id == current_user.id)
    )
    my_watchlist_count = watchlist_count_result.scalar()

    # Return a clean summary object
    return {
        "user": {
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "member_since": current_user.created_at,
        },
        "stats": {
            "total_market_items": total_market_items,
            "my_watchlist_count": my_watchlist_count,
        },
    }
