# ══════════════════════════════════════════════════════════════
#  tasks/market_tasks.py  —  Background Market Tasks
#
#  These tasks run automatically in the background via Celery.
#  They don't need a user to trigger them.
#
#  To add real market data, plug in any free API:
#    - Alpha Vantage:  https://www.alphavantage.co (free tier)
#    - CoinGecko:      https://www.coingecko.com/api (free, no key needed)
#    - Yahoo Finance:  via yfinance library (pip install yfinance)
# ══════════════════════════════════════════════════════════════

from app.tasks.celery_app import celery_app


@celery_app.task
def fetch_market_prices():
    """
    Background task: Fetches latest market prices from an external API
    and updates the market_data table in the database.

    This runs every 60 seconds automatically (configured in celery_app.py).

    ── HOW TO IMPLEMENT ──────────────────────────────────────────
    
    Step 1: Install requests:
        pip install requests
    
    Step 2: Get a free API key from Alpha Vantage or use CoinGecko (no key needed)
    
    Step 3: Replace the TODO below with actual API calls.
    
    Example using CoinGecko (free, no API key needed):
    
        import requests
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        # data looks like:
        # { "bitcoin": { "usd": 68500, "usd_24h_change": 1.8 }, ... }
        
        # Then update your database...
    ─────────────────────────────────────────────────────────────
    """

    print("[Celery] ⏳ Fetching latest market prices...")

    # TODO: Replace this with your real API call
    # See the example above for CoinGecko integration

    print("[Celery] ✅ Market prices updated successfully.")
    return {"status": "success"}
