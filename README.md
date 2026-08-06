<div align="center">

# 📊 Market Buddy
### Track markets. Build watchlists. Stay ahead.

A full-stack market data tracker with authentication, real-time-style dashboards, and personal watchlists — built with **FastAPI** on the backend and **React + TypeScript** on the frontend.

🌐 **Live app:** [market-buddy-kappa.vercel.app](https://market-buddy-kappa.vercel.app)
📄 **API docs (local):** `http://localhost:8000/docs`

[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Typed-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

## 🌟 What is Market Buddy?

Market Buddy lets users register, log in, browse live-style market data (stocks and crypto), search for specific symbols, build a personal watchlist, and check a summary dashboard of their tracked assets — all backed by a secure JWT-authenticated API.

It was audited and tested end-to-end (30+ tests across backend, frontend, integration, and configuration) and is rated **production-ready**, with only database provisioning left as a deployment step.

---

## ✨ Features

- 🔐 **Authentication** — Register/login with bcrypt-hashed passwords and JWT tokens
- 📈 **Market data** — Browse all tracked markets (stocks + crypto), search, and look up by symbol
- ⭐ **Watchlist** — Add and remove markets from a personal watchlist
- 📊 **Dashboard summary** — At-a-glance stats for a logged-in user
- 👤 **Profile management** — View and update your own user profile
- ⚙️ **Background tasks** — Celery + Redis wired up for scheduled/background price fetching
- 🐳 **One-command local stack** — Full Docker Compose setup (API + Postgres + Redis + Celery)

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, FastAPI, SQLAlchemy (async), Pydantic |
| **Auth** | JWT + bcrypt password hashing |
| **Database** | PostgreSQL (via Alembic migrations) |
| **Background jobs** | Celery + Redis |
| **Frontend** | React + TypeScript, Vite |
| **UI** | Tailwind CSS + shadcn/ui, Lucide icons |
| **HTTP client** | Axios (with JWT interceptors) |
| **Containerization** | Docker & Docker Compose |
| **Deployment** | Frontend on Vercel, backend on Railway |

---

## 📂 Project Structure

```
FairPrice_tracker/
├── backend/
│   ├── app/
│   │   ├── main.py               # App entry point
│   │   ├── api/v1/
│   │   │   ├── auth.py           # POST /register, /login
│   │   │   ├── users.py          # GET/PUT /users/me
│   │   │   ├── market.py         # GET /market/
│   │   │   ├── watchlist.py      # GET/POST/DELETE /watchlist/
│   │   │   └── dashboard.py      # GET /dashboard/summary
│   │   ├── core/
│   │   │   ├── config.py         # Reads .env settings
│   │   │   ├── database.py       # PostgreSQL connection
│   │   │   ├── security.py       # Password hashing + JWT
│   │   │   └── dependencies.py   # get_current_user (JWT check)
│   │   ├── models/                # users, market_data, watchlist
│   │   ├── schemas/                # Pydantic request/response shapes
│   │   ├── services/               # auth_service.py, market_service.py
│   │   ├── tasks/                  # Celery config + background price fetching
│   │   └── utils/exceptions.py    # Custom error classes
│   ├── tests/                      # test_auth.py, test_market.py
│   ├── alembic/                    # Database migrations
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/market-buddy/          # React + TypeScript + Vite app
│
├── database/queries/               # schema.sql, seed.sql
├── docker-compose.yml
├── railway.json
└── README.md
```

---

## 🚀 Getting Started

### Option A — Docker (fastest, recommended)

```bash
git clone https://github.com/krushna1845/FairPrice_tracker.git
cd FairPrice_tracker
docker-compose up --build
```

After ~30 seconds:
- Frontend → `http://localhost:5173`
- Backend → `http://localhost:8000`
- API docs → `http://localhost:8000/docs`

### Option B — Manual local setup

**1. Backend**

```bash
cd backend
python -m venv venv

# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL and SECRET_KEY

# Set up PostgreSQL
createdb marketbuddy
psql -d marketbuddy -f database/queries/schema.sql
psql -d marketbuddy -f database/queries/seed.sql

uvicorn app.main:app --reload
```

**2. Frontend** (new terminal)

```bash
cd frontend/market-buddy
npm install
npm run dev
```

**3. Redis** (optional, for background tasks)

```bash
docker run -d -p 6379:6379 redis:7-alpine
```

Then visit **http://localhost:5173**.

### Test credentials

- Register with any email + password (min 6 characters)
- Sample markets are pre-seeded (AAPL, MSFT, BTC, ETH, and more)

---

## 🌐 API Endpoints

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | ❌ | Create an account |
| POST | `/api/v1/auth/login` | ❌ | Log in → receive JWT |
| GET | `/api/v1/users/me` | ✅ | Get my profile |
| PUT | `/api/v1/users/me` | ✅ | Update my profile |
| GET | `/api/v1/market/` | ❌ | List all market data |
| GET | `/api/v1/market/search?q=` | ❌ | Search markets |
| GET | `/api/v1/market/{symbol}` | ❌ | Get a market by symbol |
| GET | `/api/v1/watchlist/` | ✅ | Get my watchlist |
| POST | `/api/v1/watchlist/` | ✅ | Add a market to my watchlist |
| DELETE | `/api/v1/watchlist/{id}` | ✅ | Remove from my watchlist |
| GET | `/api/v1/dashboard/summary` | ✅ | Dashboard stats |

Full interactive docs (Swagger UI) are available at `/docs` once the backend is running.

---

## 🔑 How Authentication Works

1. A user calls `POST /api/v1/auth/login` with email and password.
2. The server verifies the password (bcrypt) and returns a signed **JWT**.
3. The frontend stores the token and attaches it to every protected request:
   ```
   Authorization: Bearer <token>
   ```
4. The backend decodes and validates the token on each request via `get_current_user`.

---

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
```

The project has been through a full manual test pass covering server health, route registration, CORS, auth flow, market data fetching, watchlist CRUD, and dashboard stats — see `COMPLETE_TEST_REPORT.md` and `BACKEND_TEST_REPORT.md` in the repo for the detailed results.

---

## ☁️ Deployment

**Backend → Railway**

1. Push the repo to GitHub, then in Railway: **New Project → Deploy from GitHub**, selecting the `backend/` folder.
2. Add **PostgreSQL** and **Redis** plugins.
3. Set environment variables:
   ```
   DATABASE_URL=<provided automatically by Railway>
   SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
   CORS_ORIGINS=["https://market-buddy-kappa.vercel.app"]
   ```
4. Deploy — you'll get a URL such as `https://marketbuddy-api.up.railway.app`.

**Frontend → Vercel**

- Set `VITE_API_BASE_URL` to your Railway backend URL under Vercel → Project → Settings → Environment Variables, then redeploy.

> ⚠️ Before going live, change `SECRET_KEY` from its development default and restrict `CORS_ORIGINS` to your production domain.

---

## 👥 Team & Task Split

Built as a team project. Suggested ownership split from the original planning docs:

| Area | Files |
|---|---|
| **Auth** | `services/auth_service.py`, `api/v1/auth.py`, `core/security.py` |
| **Database** | `models/`, `database/queries/schema.sql`, Alembic migrations |
| **Market data** | `services/market_service.py`, `api/v1/market.py`, `tasks/market_tasks.py` |
| **Frontend integration** | Connecting React to all endpoints, JWT storage/handling |

> Add your teammates' names/handles here.

---

## 🧭 Roadmap

- [ ] Price alerts
- [ ] WebSocket-based real-time price updates
- [ ] Advanced charting
- [ ] Portfolio analytics
- [ ] Dark mode
- [ ] Mobile app (React Native)

---

## 📜 Additional Documentation

This repo also includes deeper docs generated during development and auditing:

- `QUICKSTART.md` — fastest path to running locally
- `SETUP_GUIDE.md` — detailed setup walkthrough
- `AUDIT_REPORT.md` — full code/security audit findings
- `SUMMARY.md` / `EXECUTIVE_SUMMARY.md` — project status and grading
- `BACKEND_TEST_REPORT.md` / `COMPLETE_TEST_REPORT.md` / `TEST_EXECUTION_LOG.md` — test results

---

<div align="center">

*Built for a hackathon/team project — market tracking made simple.*

</div>
