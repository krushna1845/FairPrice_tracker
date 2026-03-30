-- ══════════════════════════════════════════════════════════════
--  database/queries/seed.sql  —  Sample Data
--
--  Inserts sample stocks and crypto into market_data table.
--  Runs automatically when Docker starts for the first time.
--
--  ON CONFLICT DO NOTHING → won't fail if data already exists.
-- ══════════════════════════════════════════════════════════════

INSERT INTO market_data (symbol, name, price, change_percent, volume, market_cap) VALUES

    -- ── Stocks ──────────────────────────────────────────────────
    ('AAPL',  'Apple Inc.',              189.30,   1.25,  55000000,  2950000000000),
    ('MSFT',  'Microsoft Corporation',   415.20,   0.54,  18000000,  3080000000000),
    ('GOOGL', 'Alphabet Inc.',           175.50,   0.87,  22000000,  2180000000000),
    ('AMZN',  'Amazon.com Inc.',         185.60,   1.10,  32000000,  1920000000000),
    ('META',  'Meta Platforms Inc.',     505.40,   2.10,  15000000,  1290000000000),
    ('NVDA',  'NVIDIA Corporation',      875.90,   3.40,  42000000,  2160000000000),
    ('TSLA',  'Tesla Inc.',              245.80,  -2.30,  85000000,   782000000000),
    ('NFLX',  'Netflix Inc.',            610.50,   0.75,   9000000,   267000000000),
    ('AMD',   'Advanced Micro Devices',  165.40,   1.90,  35000000,   267000000000),
    ('INTC',  'Intel Corporation',        35.20,  -0.60,  28000000,   148000000000),

    -- ── Crypto ──────────────────────────────────────────────────
    ('BTC',   'Bitcoin',              68500.00,   1.80,    500000,  1340000000000),
    ('ETH',   'Ethereum',              3500.00,   2.20,   1200000,   420000000000),
    ('BNB',   'BNB',                    580.00,   0.90,    800000,    86000000000),
    ('SOL',   'Solana',                 175.00,   3.50,   2000000,    81000000000),
    ('XRP',   'XRP',                      0.58,  -0.40,  45000000,    32000000000)

ON CONFLICT (symbol) DO NOTHING;
