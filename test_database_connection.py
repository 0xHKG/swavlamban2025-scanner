#!/usr/bin/env python3
"""
Test Database Connection - Verify PostgreSQL/SQLite usage
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.core.database import engine, SQLALCHEMY_DATABASE_URL
from sqlalchemy import text

def test_database_connection():
    """Test database connection and verify PostgreSQL or SQLite"""
    print("=" * 70)
    print("DATABASE CONNECTION TEST - Swavlamban 2025")
    print("=" * 70)

    print(f"\n📊 Database URL: {SQLALCHEMY_DATABASE_URL}")

    # Determine database type
    if "postgresql" in SQLALCHEMY_DATABASE_URL:
        print("🗄️  Database Type: PostgreSQL (Production)")
    elif "sqlite" in SQLALCHEMY_DATABASE_URL:
        print("🗄️  Database Type: SQLite (Local Development)")
    else:
        print("⚠️  Database Type: Unknown")

    # Test connection
    print("\n🔌 Testing connection...")
    try:
        with engine.connect() as connection:
            # Test query
            if "postgresql" in SQLALCHEMY_DATABASE_URL:
                result = connection.execute(text("SELECT version();"))
                version = result.fetchone()[0]
                print(f"✅ Connected to PostgreSQL!")
                print(f"   Version: {version[:50]}...")
            else:
                result = connection.execute(text("SELECT sqlite_version();"))
                version = result.fetchone()[0]
                print(f"✅ Connected to SQLite!")
                print(f"   Version: {version}")

        print("\n" + "=" * 70)
        print("✅ DATABASE CONNECTION SUCCESSFUL!")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n" + "=" * 70)
        print("❌ DATABASE CONNECTION FAILED!")
        print("=" * 70)
        return False

if __name__ == "__main__":
    test_database_connection()
