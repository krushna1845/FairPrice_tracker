#!/usr/bin/env python
"""Initialize database schema using Alembic"""
import subprocess
import sys

try:
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        check=True,
        capture_output=True,
        text=True
    )
    print("✅ Database initialized successfully!")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to initialize database")
    print(f"Error: {e.stderr}")
    sys.exit(1)
