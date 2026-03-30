# ══════════════════════════════════════════════════════════════
#  models/market_data.py  —  Market Data Database Model
#
#  Maps to the "market_data" table in PostgreSQL.
#  Stores prices and info for stocks, crypto, or any market item.
#
#  Example rows:
#    AAPL  | Apple Inc.    | 189.30 | +1.25%
#    BTC   | Bitcoin       | 68500  | +1.80%
#    GOOGL | Alphabet Inc. | 175.50 | +0.87%
# ══════════════════════════════════════════════════════════════

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Numeric, BigInteger, DateTime
from app.core.database import GUID

from app.core.database import Base


class MarketData(Base):
    """
    Represents a row in the "market_data" table.

    Table columns:
        id              → unique identifier
        symbol          → ticker symbol, e.g. "AAPL", "BTC"
        name            → full name, e.g. "Apple Inc."
        price           → current market price
        change_percent  → % change today, e.g. +1.25 or -2.30
        volume          → number of units traded today
        market_cap      → total market capitalization
        last_updated    → when price was last refreshed
    """

    __tablename__ = "market_data"

    id = Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    symbol = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(150))
    price = Column(Numeric(18, 4))           # Up to 18 digits, 4 decimal places
    change_percent = Column(Numeric(8, 4))   # e.g. 1.2500 = +1.25%
    volume = Column(BigInteger)              # Large numbers (billions)
    market_cap = Column(Numeric(24, 2), nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<MarketData symbol={self.symbol} price={self.price}>"
