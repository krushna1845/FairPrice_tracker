-- ══════════════════════════════════════════════════════════════
--  queries/debug_queries.sql  —  Debug SQL Queries
--
--  Raw SQL queries used in debug_auth.py for testing database connection
--  and checking table existence.
-- ══════════════════════════════════════════════════════════════

-- Test database connection
SELECT 1;

-- Check if users table exists
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public' AND table_name='users';