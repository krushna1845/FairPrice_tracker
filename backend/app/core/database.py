# ══════════════════════════════════════════════════════════════
#  core/database.py  —  Database Connection & Session
#
#  Sets up the async connection to PostgreSQL.
#  All database operations in this app use async/await,
#  which means they don't block the server while waiting for DB.
#
#  HOW IT WORKS:
#    1. `engine`           → the actual connection to PostgreSQL
#    2. `AsyncSessionLocal` → a factory that creates DB sessions
#    3. `get_db()`          → a dependency injected into API routes
#    4. `Base`              → parent class for all SQLAlchemy models
# ══════════════════════════════════════════════════════════════

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid


# ── Step 1: Create the Async Engine ────────────────────────────
# This is the actual connection pool to PostgreSQL.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # When DEBUG=True, prints every SQL query to console
    future=True,
)


# ── Step 2: Session Factory ─────────────────────────────────────
# A "session" is like a temporary workspace for DB operations.
# You open a session → do queries → close the session.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Keep data accessible after commit
)


# ── Step 3: Base Model Class ────────────────────────────────────
# All SQLAlchemy models (User, MarketData, Watchlist) inherit from this.
class Base(DeclarativeBase):
    pass


# Cross-database GUID type: stores as native UUID on Postgres, CHAR(36) on others
class GUID(TypeDecorator):
    impl = CHAR

    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=False))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return str(value)
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        try:
            return uuid.UUID(value)
        except Exception:
            return value


# ── Step 4: Database Dependency ─────────────────────────────────
# This function is injected into API routes using FastAPI's Depends().
# It opens a session, gives it to the route, then closes it automatically.
#
# Usage in a route:
#   async def my_route(db: AsyncSession = Depends(get_db)):
#       result = await db.execute(...)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session          # Hand the session to the route
            await session.commit() # Auto-commit if no errors
        except Exception:
            await session.rollback()  # Undo changes if something fails
            raise
        finally:
            await session.close()  # Always close the session
