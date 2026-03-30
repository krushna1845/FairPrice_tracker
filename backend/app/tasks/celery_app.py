# ══════════════════════════════════════════════════════════════
#  tasks/celery_app.py  —  Celery Configuration
#
#  Celery runs BACKGROUND TASKS — work that happens automatically
#  without a user making an API request.
#
#  Example use case for Market Buddy:
#    → Every 60 seconds, fetch latest prices from an external API
#      and update the market_data table in PostgreSQL.
#
#  Celery uses Redis as a message broker (the "post office"
#  that delivers tasks to workers).
#
#  Run the worker:
#    celery -A app.tasks.celery_app worker --loglevel=info
# ══════════════════════════════════════════════════════════════

from celery import Celery
from app.core.config import settings


# Create the Celery app
celery_app = Celery(
    "market_buddy",
    broker=settings.REDIS_URL,    # Redis receives task messages
    backend=settings.REDIS_URL,   # Redis stores task results
    include=["app.tasks.market_tasks"],  # Load this task file
)

# Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    # ── Scheduled Tasks (like a cron job) ──────────────────────
    # Runs `fetch_market_prices` every 60 seconds automatically
    beat_schedule={
        "update-market-prices-every-minute": {
            "task": "app.tasks.market_tasks.fetch_market_prices",
            "schedule": 60.0,  # seconds
        },
    },
)
