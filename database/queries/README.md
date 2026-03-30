# 📁 Database Queries Folder

This folder contains all database-related SQL files for the Market Buddy project.

## 📄 Files

### schema.sql
- **Purpose**: Defines the database schema (tables, indexes, constraints)
- **Tables Created**:
  - `users` - User accounts
  - `market_data` - Stock/crypto market data
  - `watchlist` - User watchlists
- **Usage**: Run once to set up database structure

### seed.sql
- **Purpose**: Inserts initial sample data
- **Data**: Sample stocks (AAPL, MSFT, etc.) and cryptocurrencies (BTC, ETH, etc.)
- **Usage**: Run after schema to populate with test data

### debug_queries.sql
- **Purpose**: SQL queries used for debugging and connection testing
- **Location**: Used in `backend/debug_auth.py`
- **Queries**:
  - Connection test: `SELECT 1`
  - Table existence check

### test_queries.sql
- **Purpose**: SQL queries used in system testing
- **Location**: Used in `backend/scripts/test_full_system.py`
- **Queries**:
  - List all tables
  - Count rows in tables

## 🚀 How to Run

### PostgreSQL Setup
```bash
# Create database
createdb marketbuddy

# Run schema
psql -d marketbuddy -f queries/schema.sql

# Run seed data
psql -d marketbuddy -f queries/seed.sql
```

### MySQL Setup (if needed)
```bash
# Create database
mysql -u root -p -e "CREATE DATABASE marketbuddy;"

# Run schema
mysql -u root -p marketbuddy < queries/schema.sql

# Run seed data
mysql -u root -p marketbuddy < queries/seed.sql
```

## 📊 Database Structure

```
users (id, name, email, hashed_password, role, is_active, created_at)
market_data (id, symbol, name, price, change_percent, volume, market_cap, last_updated)
watchlist (id, user_id, market_data_id, added_at)
```

## 🔗 Relationships
- `watchlist.user_id` → `users.id` (CASCADE DELETE)
- `watchlist.market_data_id` → `market_data.id` (CASCADE DELETE)