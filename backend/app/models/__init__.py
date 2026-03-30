# Import all models here so Alembic can detect them during migrations.
# If you add a new model file, import it here too.

from app.core.database import Base
from app.models.user import User
from app.models.market_data import MarketData
from app.models.watchlist import Watchlist
