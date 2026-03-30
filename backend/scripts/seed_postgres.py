#!/usr/bin/env python3
"""
Seed PostgreSQL database with initial data.
Run this after creating the database and running migrations.
"""

import psycopg2
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

def seed_database():
    """Seed the database with initial data."""
    try:
        # Parse the DATABASE_URL
        from urllib.parse import urlparse
        parsed = urlparse(settings.DATABASE_URL.replace('+asyncpg', ''))

        # Connect to our database
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path.lstrip('/')
        )
        cursor = conn.cursor()

        # Read seed.sql
        seed_file = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'queries', 'seed.sql')
        with open(seed_file, 'r') as f:
            seed_sql = f.read()

        # Execute seed SQL
        cursor.execute(seed_sql)
        conn.commit()

        print("Database seeded successfully.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    seed_database()