# 🚀 Market Buddy - Quick Start Guide

## Prerequisites Installed ✅

- ✅ Python 3.11+ (Backend)
- ✅ Node.js + npm (Frontend)  
- ✅ PostgreSQL (Database)
- ✅ Docker & Docker Compose (All-in-one option)
- ✅ Redis (Caching)

---

## 🔧 Setup & Run - Choose Your Option

### Setup Instructions

#### Backend Setup:

```bash
# 1. Navigate to backend folder
cd backend

# 2. Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# OR Mac/Linux:
source venv/bin/activate

# 3. Install Python packages
pip install -r requirements.txt

# 4. Make sure .env exists (already created for you ✅)
# Check: cat .env

# 5. Start PostgreSQL database
# Make sure PostgreSQL service is running on your machine
# 6. Initialize database (first time only)
alembic upgrade head

# 7. Load seed data (first time only)
# psql -d marketbuddy -U postgres < database/queries/schema.sql
# psql -d marketbuddy -U postgres < database/queries/seed.sql

# 8. Start backend server
uvicorn app.main:app --reload

# Visit: http://localhost:8000/docs (API documentation)
```

#### Frontend Setup:

```bash
# 1. Navigate to frontend folder
cd frontend/market-buddy

# 2. Install dependencies
npm install

# 3. Check .env file exists (already created for you ✅)
# cat .env
# Should show: VITE_API_BASE_URL=http://localhost:8000

# 4. Start dev server
npm run dev

# Visit: http://localhost:5173
```

#### Redis Setup (Optional - for Celery tasks):

```bash
# Install locally (Windows)
# Download from: https://github.com/microsoftarchive/redis/releases
# Or use WSL: wsl -d Ubuntu apt-get install redis-server
```

---

## 🧪 Test the Application

### 1. Test Backend API

```bash
# Open API Documentation
http://localhost:8000/docs

# OR Test with curl:

# Register new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'

# Get all market data
curl "http://localhost:8000/api/v1/market/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 2. Test Frontend

```bash
# 1. Open http://localhost:5173 in browser
# 2. You should see login page (FairPrice Tracker)
# 3. Try logging in with credentials from database:
#    - Email: any email you registered
#    - Password: the password you registered with
```

### 3. Test Full Flow

```bash
# 1. Run backend (Terminal 1)
cd backend
uvicorn app.main:app --reload

# 2. Run frontend (Terminal 2)
cd frontend/market-buddy
npm run dev

# 3. Run Redis (Terminal 3 - optional)
redis-server
# OR: docker run -d -p 6379:6379 redis:7-alpine

# 4. Open browser: http://localhost:5173
# 5. Register new account or login
# 6. View market data
# 7. Add to watchlist
```

---

## 📊 Database

### Check Database Contents

```bash
# Connect to PostgreSQL
psql -d marketbuddy -U postgres

# List tables
\dt

# Check users
SELECT id, name, email, created_at FROM users;

# Check market data
SELECT symbol, name, price, change_percent FROM market_data;

# Check watchlist
SELECT * FROM watchlist;

# Exit
\q
```

---

## 🔑 Sample Test Credentials

**From seed.sql (pre-loaded data):**

**Market Data (Already Seeded):**
- AAPL - Apple Inc. ($189.30)
- MSFT - Microsoft ($415.20)
- BTC - Bitcoin ($68,500)
- ETH - Ethereum ($3,500)
- GOOGL - Alphabet Inc. ($175.50)

**Create test user via API:**
```bash
POST http://localhost:8000/api/v1/auth/register

{
  "name": "Test User",
  "email": "test@example.com",
  "password": "testpass123"
}

# Response includes: access_token, user_id, name, email
```

---

## 🛑 Troubleshooting

### "Cannot connect to database"
```bash
# Check if PostgreSQL is running
# Windows: Services > Look for "PostgreSQL"
# Docker: docker ps | grep postgres

# If not running, start it:
docker run -d -p 5432:5432 \
  -e POSTGRES_DB=marketbuddy \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  postgres:16-alpine
```

### "Cannot connect to Redis"
```bash
# Not required for basic testing, only for Celery tasks
# If you need it: docker run -d -p 6379:6379 redis:7-alpine
```

### "Frontend shows blank/errors"
```bash
# Check browser console (F12)
# Make sure backend is running on http://localhost:8000
# Check .env: VITE_API_BASE_URL=http://localhost:8000
```

### "Login fails with 'Invalid credentials'"
```bash
# 1. Make sure you're using correct email/password
# 2. Check backend console for error messages
# 3. Verify database has user data: psql -d marketbuddy -U postgres
```

### "Port 8000 already in use"
```bash
# Find what's using port 8000:
netstat -ano | findstr :8000
# Kill the process:
taskkill /PID <PID> /F
# OR use different port:
uvicorn app.main:app --reload --port 8001
```

### "Port 5173 already in use"
```bash
# Use different port:
npm run dev -- --port 3000
```

---

## 📦 Project Structure Reference

```
Market-buddy/
├── backend/                    # Python FastAPI server
│   ├── app/
│   │   ├── main.py             # Entry point
│   │   ├── api/v1/             # API routes
│   │   ├── core/               # Config, Security, Database
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   └── tasks/              # Celery background tasks
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Container image
│   ├── .env                    # Environment variables ✅ CREATED
│   └── alembic/                # Database migrations
│
├── frontend/market-buddy/      # React + TypeScript
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API client ✅ CREATED
│   │   ├── pages/              # Page components
│   │   ├── lib/                # Utilities
│   │   └── App.tsx             # Root component
│   ├── package.json            # Dependencies (axios added ✅)
│   ├── .env                    # Frontend vars ✅ CREATED
│   ├── vite.config.ts          # Vite config
│   └── tsconfig.json           # TypeScript config
│
├── database/
│   ├── schema.sql              # Table definitions
│   └── seed.sql                # Sample data
│
├── AUDIT_REPORT.md             # ✅ Full audit & issues
└── SETUP_GUIDE.md              # ✅ This file
```

---

## ✅ What's Already Fixed

1. ✅ `.env` file created for backend
2. ✅ `.env` file created for frontend  
3. ✅ API service file created (`src/services/api.ts`)
4. ✅ LoginPage updated to use backend auth
5. ✅ Axios added to dependencies
6. ✅ JWT token handling implemented
7. ✅ Request/Response interceptors set up

---

## 🚀 Next Steps After Running

1. **Test Authentication**
   - Register new user
   - Login
   - Verify token stored in localStorage

2. **Test Market Data**
   - View all market items
   - Search for items
   - Check real-time prices

3. **Test Watchlist**
   - Add items to watchlist
   - View your watchlist
   - Remove items

4. **Test Dashboard** (if implemented)
   - View market summary
   - Check portfolio

---

## 📝 Important Notes

- **Local Storage:** JWT tokens are stored in browser localStorage
- **CORS:** Backend allows requests from http://localhost:3000 and http://localhost:5173
- **API Documentation:** Visit http://localhost:8000/docs when backend is running
- **Default Port:** Frontend on 5173, Backend on 8000
- **Database:** PostgreSQL runs on 5432 (Docker Compose) or system PostgreSQL

---

## 🎯 Production Deployment

Before deploying to production:

1. Change `SECRET_KEY` in backend `.env`
2. Update `CORS_ORIGINS` to your domain
3. Set `DEBUG=False` in backend
4. Use environment-specific `.env` files
5. Set up proper HTTPS/SSL
6. Use managed database (AWS RDS, Azure Database)
7. Use managed Redis (AWS ElastiCache, Azure Cache)
8. Deploy frontend to Vercel (already configured)
9. Deploy backend to production server (Heroku, AWS, Azure)

---

## 📞 Support

- **API Docs:** http://localhost:8000/docs
- **Backend Issues:** Check `backend/` folder structure
- **Frontend Issues:** Check browser console (F12)
- **Database Issues:** Use `psql` to debug
- **Docker Issues:** `docker-compose logs servicename`

---

Generated: 2026-02-23  
Status: Ready to Deploy ✅
