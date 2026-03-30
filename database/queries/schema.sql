-- ══════════════════════════════════════════════════════════════
--  database/queries/schema.sql  —  PostgreSQL Table Definitions
--
--  This file creates all tables when the Docker container starts.
--  You don't need to run this manually — Docker handles it.
--
--  Tables:
--    1. users        → stores registered user accounts
--    2. market_data  → stores stock/crypto prices and info
--    3. watchlist    → links users to their saved market items
-- ══════════════════════════════════════════════════════════════

-- Enable UUID generation (needed for gen_random_uuid())
CREATE EXTENSION IF NOT EXISTS "pgcrypto";


-- ── Table 1: Users ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id               UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    name             VARCHAR(100) NOT NULL,
    email            VARCHAR(150) NOT NULL UNIQUE,
    hashed_password  VARCHAR(255) NOT NULL,
    role             VARCHAR(20)  DEFAULT 'USER',     -- 'USER' or 'ADMIN'
    is_active        BOOLEAN      DEFAULT TRUE,
    created_at       TIMESTAMP    DEFAULT NOW()
);


-- ── Table 2: Market Data ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS market_data (
    id              UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol          VARCHAR(50)   NOT NULL UNIQUE,    -- e.g. 'AAPL', 'BTC'
    name            VARCHAR(150),                     -- e.g. 'Apple Inc.'
    price           NUMERIC(18,4),                    -- e.g. 189.3000
    change_percent  NUMERIC(8,4),                     -- e.g. 1.2500 means +1.25%
    volume          BIGINT,                           -- trading volume
    market_cap      NUMERIC(24,2),                    -- market capitalization
    last_updated    TIMESTAMP     DEFAULT NOW()
);


-- ── Table 3: Watchlist ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS watchlist (
    id              UUID      PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    market_data_id  UUID      NOT NULL REFERENCES market_data(id) ON DELETE CASCADE,
    added_at        TIMESTAMP DEFAULT NOW(),

    -- Prevent a user from adding the same item twice
    UNIQUE(user_id, market_data_id)
);


-- ── Indexes for faster queries ─────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_users_email         ON users(email);
CREATE INDEX IF NOT EXISTS idx_market_symbol       ON market_data(symbol);
CREATE INDEX IF NOT EXISTS idx_watchlist_user_id   ON watchlist(user_id);
