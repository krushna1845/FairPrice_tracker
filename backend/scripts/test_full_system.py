#!/usr/bin/env python
"""
Comprehensive system health check:
- Database connection
- Tables and data count
- API endpoints test
- Storage location info
"""
import sys
import os
import asyncio
import json
from urllib.parse import urlparse, unquote

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings


async def test_database():
    """Test database connection and inspect tables."""
    print("\n" + "="*70)
    print("🔍 DATABASE CONNECTION TEST")
    print("="*70)
    
    database_url = settings.DATABASE_URL
    print(f"\n📋 Database URL: {database_url}")
    
    # Parse URL
    url = urlparse(database_url)
    db_type = url.scheme.split('+')[0]  # 'postgresql' or 'mysql'
    user = unquote(url.username) if url.username else 'unknown'
    host = url.hostname or 'localhost'
    port = url.port or (5432 if db_type == 'postgresql' else 3306)
    db_name = url.path.lstrip('/') or 'unknown'
    
    print(f"   Type: {db_type.upper()}")
    print(f"   Host: {host}:{port}")
    print(f"   User: {user}")
    print(f"   Database: {db_name}")
    
    # Try connection based on DB type
    try:
        if 'mysql' in db_type:
            print("\n🔌 Attempting MySQL connection...")
            import aiomysql
            password = unquote(url.password) if url.password else ''
            conn = await aiomysql.connect(
                host=host, 
                port=port, 
                user=user, 
                password=password,
                db=db_name,
                autocommit=True
            )
            
            cur = await conn.cursor()
            
            # Get tables
            await cur.execute("SHOW TABLES;")
            tables = await cur.fetchall()
            print(f"   ✅ Connected! Found {len(tables)} tables: {[t[0] for t in tables]}")
            
            # Check data in each table
            for table in tables:
                table_name = table[0]
                await cur.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = await cur.fetchone()
                print(f"      - {table_name}: {count[0]} rows")
            
            await cur.close()
            conn.close()
            
        elif 'postgresql' in db_type:
            print("\n🔌 Attempting PostgreSQL connection...")
            import asyncpg
            password = unquote(url.password) if url.password else ''
            conn = await asyncpg.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name
            )
            
            # Get tables
            tables = await conn.fetch(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
            )
            print(f"   ✅ Connected! Found {len(tables)} tables: {[t['table_name'] for t in tables]}")
            
            # Check data in each table
            for table in tables:
                table_name = table['table_name']
                count = await conn.fetchval(f"SELECT COUNT(*) FROM {table_name};")
                print(f"      - {table_name}: {count} rows")
            
            await conn.close()
            
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    return True


async def test_api():
    """Test API endpoints."""
    print("\n" + "="*70)
    print("🌐 API ENDPOINTS TEST")
    print("="*70)
    
    import httpx
    
    base_url = "http://127.0.0.1:4000"
    endpoints = [
        ("GET", "/", "Health check"),
        ("GET", "/api/v1/market/", "List all market items"),
        ("GET", "/api/v1/market/AAPL", "Get specific market item by symbol"),
        ("GET", "/api/v1/market/search?q=Apple", "Search market items by name"),
        ("POST", "/api/v1/auth/register", "Register user (should fail or require fields)"),
        ("POST", "/api/v1/auth/login", "Login user (should fail with wrong credentials)"),
    ]
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            for method, path, description in endpoints:
                try:
                    print(f"\n📡 {method} {base_url}{path}")
                    print(f"   Description: {description}")
                    
                    if method == "GET":
                        resp = await client.get(f"{base_url}{path}")
                    elif method == "POST":
                        if "register" in path:
                            resp = await client.post(f"{base_url}{path}", json={})
                        elif "login" in path:
                            resp = await client.post(f"{base_url}{path}", json={"email": "test@example.com", "password": "wrong"})
                    
                    print(f"   Status: {resp.status_code}")
                    if resp.status_code < 500:
                        try:
                            data = resp.json()
                            if isinstance(data, list):
                                print(f"   ✅ Response: {len(data)} items returned")
                                if len(data) > 0:
                                    print(f"      Sample: {json.dumps(data[0], indent=6)[:200]}...")
                            else:
                                print(f"   ✅ Response: {json.dumps(data, indent=6)[:200]}...")
                        except:
                            print(f"   Response (text): {resp.text[:200]}")
                    else:
                        print(f"   ❌ Error: {resp.text[:200]}")
                        
                except Exception as e:
                    print(f"   ❌ Request failed: {e}")
                    
    except Exception as e:
        print(f"\n❌ API test failed: {e}")
        print("   (Is the backend running at http://127.0.0.1:4000?)")


def print_storage_info():
    """Tell user where data is stored."""
    print("\n" + "="*70)
    print("💾 DATA STORAGE LOCATION")
    print("="*70)
    
    url = urlparse(settings.DATABASE_URL)
    db_type = url.scheme.split('+')[0]
    host = url.hostname or 'localhost'
    db_name = url.path.lstrip('/')or 'marketbuddy'
    
    print(f"\n📍 Database: {db_type.upper()}")
    print(f"🖥️  Host: {host}")
    print(f"📦 Database Name: {db_name}")
    
    if 'mysql' in db_type:
        print(f"\n📂 Data files location (typical):")
        print(f"   Windows: C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Data\\{db_name}\\")
        print(f"   Linux: /var/lib/mysql/{db_name}/")
        print(f"   macOS: /usr/local/var/mysql/{db_name}/")
        
    elif 'postgresql' in db_type:
        print(f"\n📂 Data files location (typical):")
        print(f"   Windows: C:\\Program Files\\PostgreSQL\\15\\data\\base\\")
        print(f"   Linux: /var/lib/postgresql/15/main/")
        print(f"   macOS: /usr/local/var/postgres/")
    
    print(f"\n📊 Tables storing data:")
    print(f"   • users → User accounts and profiles")
    print(f"   • market_data → Stock/crypto prices and info")
    print(f"   • watchlist → User's watched items")


async def main():
    """Run all tests."""
    print("\n" + "🎯 MARKET BUDDY - SYSTEM HEALTH CHECK 🎯".center(70))
    
    # Test database
    db_ok = await test_database()
    
    # Test API (if backend is running)
    print("\n⏳ Attempting to reach backend API...")
    import httpx
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get("http://127.0.0.1:4000/")
            print("✅ Backend is running!")
            await test_api()
    except Exception as e:
        print(f"⚠️  Backend not running: {e}")
        print("   Start it with: uvicorn app.main:app --reload --port 4000")
    
    # Show storage info
    print_storage_info()
    
    print("\n" + "="*70)
    print("✅ System check complete!")
    print("="*70 + "\n")


if __name__ == '__main__':
    asyncio.run(main())
