#!/usr/bin/env python3
"""
Create PostgreSQL database for Market Buddy.
Run this script once to set up the database.
"""

import psycopg2
from psycopg2 import sql
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

def create_database():
    """Create the database if it doesn't exist."""
    # Connect to default postgres database to create our database
    try:
        # Parse the DATABASE_URL to get connection details
        from urllib.parse import urlparse
        parsed = urlparse(settings.DATABASE_URL.replace('+asyncpg', ''))  # Remove asyncpg for psycopg2

        # Connect to postgres database (default) - no password for local trust
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            user=parsed.username,
            database='postgres'  # Connect to default postgres db
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (parsed.path.lstrip('/'),))
        exists = cursor.fetchone()

        if not exists:
            # Create database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(parsed.path.lstrip('/'))
            ))
            print(f"Database '{parsed.path.lstrip('/')}' created successfully.")
        else:
            print(f"Database '{parsed.path.lstrip('/')}' already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()