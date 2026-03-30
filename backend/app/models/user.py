# ══════════════════════════════════════════════════════════════
#  models/user.py  —  User Database Model
#
#  This Python class maps directly to the "users" table in PostgreSQL.
#  Each attribute = one column in the table.
#
#  SQLAlchemy will use this class to:
#    - CREATE the table (via Alembic migrations)
#    - INSERT new users
#    - SELECT / UPDATE / DELETE users
# ══════════════════════════════════════════════════════════════

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime
from app.core.database import GUID

from app.core.database import Base


class User(Base):
    """
    Represents a row in the "users" table.

    Table columns:
        id               → unique identifier (UUID)
        name             → user's full name
        email            → unique login email
        hashed_password  → bcrypt hash (never store plain passwords!)
        role             → "USER" or "ADMIN"
        is_active        → False = account disabled
        created_at       → when the account was made
    """

    __tablename__ = "users"

    id = Column(
        GUID(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),   # Auto-generate a unique UUID for each new user
    )
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="USER")        # "USER" or "ADMIN"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        # What shows up when you print a User object
        return f"<User id={self.id} email={self.email}>"
