-- ══════════════════════════════════════════════════════════════
--  queries/test_queries.sql  —  Test SQL Queries
--
--  Raw SQL queries used in test_full_system.py for validating database
--  setup and checking data counts.
-- ══════════════════════════════════════════════════════════════

-- Get all table names in public schema
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public';

-- Count rows in a specific table (parameterized)
-- Usage: SELECT COUNT(*) FROM {table_name};
-- Example: SELECT COUNT(*) FROM users;