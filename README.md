# 🚀 Market Buddy — Backend (Python FastAPI)

Frontend is live at: **https://market-buddy-kappa.vercel.app**  
Backend API docs: **http://localhost:8000/docs** (after starting locally)

---

## 📁 Folder Structure

```
backend/
├── app/
│   ├── main.py              ← App entry point. Start here.
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py      ← POST /register, /login
│   │       ├── users.py     ← GET/PUT /users/me
│   │       ├── market.py    ← GET /market/
│   │       ├── watchlist.py ← GET/POST/DELETE /watchlist/
│   │       └── dashboard.py ← GET /dashboard/summary
│   ├── core/
│   │   ├── config.py        ← Read .env settings
│   │   ├── database.py      ← PostgreSQL connection
│   │   ├── security.py      ← Password hashing + JWT
│   │   └── dependencies.py  ← get_current_user (JWT check)
│   ├── models/
│   │   ├── user.py          ← users table
│   │   ├── market_data.py   ← market_data table
│   │   └── watchlist.py     ← watchlist table
│   ├── schemas/
│   │   ├── auth.py          ← Register/Login request + response shapes
│   │   ├── user.py          ← User response shape
│   │   └── market.py        ← Market/Watchlist shapes
│   ├── services/
│   │   ├── auth_service.py  ← Register & login logic
│   │   └── market_service.py← Market & watchlist logic
│   ├── tasks/
│   │   ├── celery_app.py    ← Celery config
│   │   └── market_tasks.py  ← Background price fetching
│   └── utils/
│       └── exceptions.py    ← Custom error classes
├── tests/
│   ├── test_auth.py         ← Auth API tests
│   └── test_market.py       ← Market API tests
├── alembic/                 ← Database migrations
├── requirements.txt         ← Python packages
├── .env.example             ← Copy to .env
└── Dockerfile
```

---

## ⚡ Getting Started

### Run locally

**1. Create virtual environment**
```bash
cd backend
python -m venv venv

# Mac / Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

**2. Install packages**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
cp .env.example .env
# Open .env and fill in your DATABASE_URL and SECRET_KEY
```

**4. Set up PostgreSQL database**
```bash
# Make sure PostgreSQL is running, then:
createdb marketbuddy

# Run schema + seed data:
psql -d marketbuddy -f database/queries/schema.sql
psql -d marketbuddy -f database/queries/seed.sql
```

**5. Start the server**
```bash
uvicorn app.main:app --reload
```

---

## 🌐 API Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /api/v1/auth/register | ❌ No | Create account |
| POST | /api/v1/auth/login | ❌ No | Login → get token |
| GET | /api/v1/users/me | ✅ Yes | My profile |
| PUT | /api/v1/users/me | ✅ Yes | Update profile |
| GET | /api/v1/market/ | ❌ No | All market data |
| GET | /api/v1/market/search?q= | ❌ No | Search |
| GET | /api/v1/market/{symbol} | ❌ No | Get by symbol |
| GET | /api/v1/watchlist/ | ✅ Yes | My watchlist |
| POST | /api/v1/watchlist/ | ✅ Yes | Add to watchlist |
| DELETE | /api/v1/watchlist/{id} | ✅ Yes | Remove from watchlist |
| GET | /api/v1/dashboard/summary | ✅ Yes | Dashboard stats |

**Test all endpoints visually at: http://localhost:8000/docs**

---

## 🔑 How Authentication Works

1. User calls `POST /api/v1/auth/login` with email + password
2. Server returns a **JWT token** (a long string)
3. Frontend stores the token (in localStorage or cookies)
4. For every protected request, frontend sends:
   ```
   Authorization: Bearer eyJhbGci...your_token_here...
   ```
5. Server decodes the token to know who's making the request

---

## 🧪 Run Tests
```bash
pytest tests/ -v
```

---

## 🚀 Deploy to Railway (Free)

1. Push your code to GitHub
2. Go to https://railway.app → **New Project** → Deploy from GitHub
3. Select your repo → choose the `backend/` folder
4. Click **Add Plugin** → add **PostgreSQL** → add **Redis**
5. Go to **Variables** tab and add:
   ```
   DATABASE_URL=<Railway gives you this automatically>
   SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
   CORS_ORIGINS=["https://market-buddy-kappa.vercel.app"]
   ```
6. Deploy! You'll get a URL like `https://marketbuddy-api.up.railway.app`

**Then update your Vercel frontend:**
- Go to Vercel → your project → Settings → Environment Variables
- Add: `VITE_API_BASE_URL = https://marketbuddy-api.up.railway.app`
- Redeploy the frontend

---

## 👥 Team Task Split

| Member | File(s) to work on |
|--------|-------------------|
| Auth   | `services/auth_service.py`, `api/v1/auth.py`, `core/security.py` |
| DB     | `models/`, `database/queries/schema.sql`, Alembic migrations |
| Market | `services/market_service.py`, `api/v1/market.py`, `tasks/market_tasks.py` |
| Frontend Integration | Connect React to all endpoints, handle JWT storage |
