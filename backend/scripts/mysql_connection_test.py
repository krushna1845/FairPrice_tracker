#!/usr/bin/env python
"""Quick async MySQL connection test using aiomysql.

Steps:
 - Reads `DATABASE_URL` from `app.core.config.settings`
 - Connects as configured user (root in your case)
 - Ensures database exists
 - Creates a small table, inserts a row, reads it back

Run after activating venv and installing requirements::

    # Windows PowerShell
    .\\venv\\Scripts\\Activate
    pip install -r requirements.txt
    python .\\scripts\\mysql_connection_test.py

This script prints status lines and exits with non-zero on error.
"""
import asyncio
import sys
import os
from urllib.parse import urlparse, unquote

try:
    import aiomysql
except Exception:
    print("aiomysql not installed. Run: pip install aiomysql")
    raise

# Ensure project package `app` is importable when running this script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.config import settings


async def main():
    url = urlparse(settings.DATABASE_URL)
    user = unquote(url.username) if url.username else 'root'
    password = unquote(url.password) if url.password else ''
    host = url.hostname or 'localhost'
    port = url.port or 3306
    dbname = url.path.lstrip('/') or 'marketbuddy'

    print(f"Connecting to MySQL {host}:{port} as {user}")
    try:
        conn = await aiomysql.connect(host=host, port=port, user=user, password=password, autocommit=True)
    except Exception as e:
        print("Failed to connect:", e)
        raise

    async with conn:
        cur = await conn.cursor()
        try:
            print(f"Ensuring database '{dbname}' exists...")
            await cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            await cur.execute(f"USE `{dbname}`;")

            print("Creating test table and inserting a row...")
            await cur.execute("CREATE TABLE IF NOT EXISTS test_connection (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100));")
            await cur.execute("INSERT INTO test_connection (name) VALUES ('connection_test')")
            await cur.execute("SELECT id, name FROM test_connection ORDER BY id DESC LIMIT 1;")
            row = await cur.fetchone()
            print("Row inserted and read back:", row)
            print("SUCCESS: MySQL connection and simple CRUD worked.")
        finally:
            await cur.close()


if __name__ == '__main__':
    asyncio.run(main())
