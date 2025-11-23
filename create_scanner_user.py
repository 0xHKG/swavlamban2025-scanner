#!/usr/bin/env python3
"""
Create test scanner user account for testing the Scanner PWA
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.core.database import SessionLocal, init_db
from app.core.security import hash_password
from app.models.user import User

def create_scanner_user():
    """Create a test scanner user account"""

    # Initialize database (creates tables if they don't exist)
    print("🗄️  Initializing database...")
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Check if scanner user already exists
        existing_user = db.query(User).filter(User.username == "scanner1").first()

        if existing_user:
            print("⚠️  Scanner user 'scanner1' already exists!")
            print("\n📋 Test Credentials:")
            print("=" * 50)
            print("Username: scanner1")
            print("Password: scanner123")
            print("Role: scanner")
            print("=" * 50)
            return

        # Create scanner user
        print("👤 Creating scanner user account...")

        scanner_user = User(
            username="scanner1",
            password_hash=hash_password("scanner123"),
            organization="Gate Operations",
            role="scanner",
            max_entries=0,  # Scanners don't create entries
            quota_ex_day1=0,
            quota_ex_day2=0,
            quota_interactive=0,
            quota_plenary=0,
            allowed_passes={},  # Scanners don't generate passes
            is_active=True
        )

        db.add(scanner_user)
        db.commit()

        print("✅ Scanner user created successfully!")
        print("\n📋 Test Credentials:")
        print("=" * 50)
        print("Username: scanner1")
        print("Password: scanner123")
        print("Organization: Gate Operations")
        print("Role: scanner")
        print("=" * 50)
        print("\n🎯 You can now login to the Scanner PWA at:")
        print("   http://localhost:3000")
        print("\n🚪 Available Gates:")
        print("   - Gate 1: Exhibition Day 1 (25 Nov)")
        print("   - Gate 2: Exhibition Day 2 (26 Nov)")
        print("   - Gate 3: Interactive Sessions (26 Nov)")
        print("   - Gate 4: Plenary Session (26 Nov)")
        print("   - Main Entrance: Date-based validation")

    except Exception as e:
        print(f"❌ Error creating scanner user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_scanner_user()
