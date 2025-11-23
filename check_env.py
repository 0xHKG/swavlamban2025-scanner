#!/usr/bin/env python3
"""
Check Environment Variables - Diagnostic Tool
Shows what environment variables are loaded
"""
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.core.config import settings

print("=" * 70)
print("ENVIRONMENT VARIABLES CHECK")
print("=" * 70)

# Check database variables
print("\n📊 DATABASE CONFIGURATION:")
print(f"  DB_HOST: {os.getenv('DB_HOST', 'NOT SET')}")
print(f"  DB_PORT: {os.getenv('DB_PORT', 'NOT SET')}")
print(f"  DB_NAME: {os.getenv('DB_NAME', 'NOT SET')}")
print(f"  DB_USER: {os.getenv('DB_USER', 'NOT SET')}")
print(f"  DB_PASSWORD: {'*' * 10 if os.getenv('DB_PASSWORD') else 'NOT SET'}")

print("\n⚙️  SETTINGS (from config.py):")
print(f"  settings.DB_HOST: {settings.DB_HOST}")
print(f"  settings.DB_PORT: {settings.DB_PORT}")
print(f"  settings.DB_NAME: {settings.DB_NAME}")
print(f"  settings.DB_USER: {settings.DB_USER}")
print(f"  settings.DB_PASSWORD: {'*' * 10}")

print("\n🗄️  DATABASE URL:")
print(f"  {settings.database_url[:50]}...")

# Check which database will be used
if os.getenv("DB_HOST") and os.getenv("DB_NAME"):
    print("\n✅ Will use: PostgreSQL (Production)")
else:
    print("\n📝 Will use: SQLite (Local Development)")

print("\n" + "=" * 70)
