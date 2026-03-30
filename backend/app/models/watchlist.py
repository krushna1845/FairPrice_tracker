# ══════════════════════════════════════════════════════════════
#  models/watchlist.py  —  Watchlist Database Model
#
#  Maps to the "watchlist" table in PostgreSQL.
#  This is a JOIN table — it links Users ↔ MarketData.
#
#  Think of it as: "User X is watching Item Y"
#
#  Example:
#    user_id: abc-123  |  market_data_id: def-456 (AAPL)
#    user_id: abc-123  |  market_data_id: ghi-789 (BTC)
#    → User abc-123 is watching AAPL and BTC
# ══════════════════════════════════════════════════════════════

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from app.core.database import GUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Watchlist(Base):
    """
    Represents a row in the "watchlist" table.

    Table columns:
        id              → unique identifier for this watchlist entry
        user_id         → which user is watching (FK → users.id)
        market_data_id  → which market item they're watching (FK → market_data.id)
        added_at        → when they added it to their watchlist

    Constraints:
        UNIQUE(user_id, market_data_id) → a user can't add the same item twice
    """

    __tablename__ = "watchlist"

    # Enforce that a user can only add the same market item once
    __table_args__ = (
        UniqueConstraint("user_id", "market_data_id", name="uq_user_market"),
    )

    id = Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key → links to the users table
    user_id = Column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),  # If user is deleted, remove their watchlist too
        nullable=False,
    )

    # Foreign key → links to the market_data table
    market_data_id = Column(
        GUID(),
        ForeignKey("market_data.id", ondelete="CASCADE"),  # If market item is deleted, remove it from all watchlists
        nullable=False,
    )

    added_at = Column(DateTime, default=datetime.utcnow)

    # Relationships: lets you do  watchlist_item.user  or  watchlist_item.market_data
    user = relationship("User", backref="watchlist_items")
    market_data = relationship("MarketData", backref="watchers")

    def __repr__(self):
        return f"<Watchlist user={self.user_id} item={self.market_data_id}>"
