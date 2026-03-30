#!/usr/bin/env python
"""
Create MySQL database and a non-root user for Market Buddy.
Run this after activating the backend venv.
"""
import sys

try:
    import pymysql
except Exception as e:
    print("Missing pymysql. Install with: pip install pymysql")
    raise

ROOT_USER = "root"
ROOT_PASS = "Krish@123"
DB_NAME = "marketbuddy"
APP_USER = "market_user"
APP_PASS = "StrongPass123"
HOST = "127.0.0.1"
PORT = 3306

def main():
    try:
        conn = pymysql.connect(host=HOST, user=ROOT_USER, password=ROOT_PASS, port=PORT, autocommit=True)
        cur = conn.cursor()
        print(f"Connected to MySQL at {HOST}:{PORT} as {ROOT_USER}")

        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"Database '{DB_NAME}' ensured")

        # Create user and grant privileges
        cur.execute(f"CREATE USER IF NOT EXISTS '{APP_USER}'@'localhost' IDENTIFIED BY '{APP_PASS}';")
        cur.execute(f"GRANT ALL PRIVILEGES ON `{DB_NAME}`.* TO '{APP_USER}'@'localhost';")
        cur.execute("FLUSH PRIVILEGES;")
        print(f"User '{APP_USER}'@'localhost' created/granted privileges")

        cur.close()
        conn.close()
        print("Done")
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
