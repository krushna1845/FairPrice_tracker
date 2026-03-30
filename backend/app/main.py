# ══════════════════════════════════════════════════════════════
#  main.py  —  Application Entry Point
#
#  This is the FIRST file FastAPI reads when it starts.
#  It:
#    1. Creates the FastAPI app
#    2. Adds CORS middleware (so your Vercel frontend can call this)
#    3. Registers all API route files
#
#  Run locally:  uvicorn app.main:app --reload
#  API Docs:     http://localhost:8000/docs
# ══════════════════════════════════════════════════════════════

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Import all route files
from app.api.v1 import auth, users, market, watchlist, dashboard


# ── Create FastAPI Application ─────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="REST API backend for Market Buddy — powering the React frontend on Vercel.",
    version="1.0.0",
    docs_url="/docs",    # Swagger UI:  http://localhost:8000/docs
    redoc_url="/redoc",  # ReDoc UI:    http://localhost:8000/redoc
)


# ── CORS Middleware ─────────────────────────────────────────────
# Without this, your browser will BLOCK requests from Vercel to this API.
# We whitelist only trusted origins (your frontend URLs).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,   # e.g. ["https://market-buddy-kappa.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],                   # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],                   # Allow Authorization, Content-Type, etc.
)


# ── Register API Routers ────────────────────────────────────────
# Each router handles a group of related endpoints.
# All endpoints are prefixed with /api/v1/

app.include_router(auth.router,      prefix="/api/v1", tags=["🔐 Auth"])
app.include_router(users.router,     prefix="/api/v1", tags=["👤 Users"])
app.include_router(market.router,    prefix="/api/v1", tags=["📈 Market"])
app.include_router(watchlist.router, prefix="/api/v1", tags=["⭐ Watchlist"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["📊 Dashboard"])


# ── Health Check ────────────────────────────────────────────────
# Visit http://localhost:8000/ to confirm the server is running.
@app.get("/", tags=["⚡ Health"])
async def health_check():
    return {
        "status": "✅ Server is running",
        "app": settings.APP_NAME,
        "api_docs": "/docs",
    }
