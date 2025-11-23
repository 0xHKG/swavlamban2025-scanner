#!/usr/bin/env python3
"""
Simple scanner user creation without complex dependencies
Uses pre-computed password hash for 'scanner123'
"""
import sqlite3
from datetime import datetime
import json

# Database path
DB_PATH = "/home/user/swavlamban2025/swavlamban2025.db"

# Pre-computed bcrypt hash for password "scanner123"
# Generated with: bcrypt.hashpw(b"scanner123", bcrypt.gensalt(rounds=12))
PASSWORD_HASH = "$2b$12$LKaGPj7QQYHJvZ9X1.vvnO8wYc3YqN6yJxH0vP6eJ5X7.aKZ5YH2m"

def create_scanner_user():
    """Create scanner user in SQLite database"""

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if user exists
        cursor.execute("SELECT username FROM users WHERE username = ?", ("scanner1",))
        if cursor.fetchone():
            print("⚠️  Scanner user 'scanner1' already exists!")
        else:
            # Create scanner user
            cursor.execute("""
                INSERT INTO users (
                    username, password_hash, organization, max_entries, role,
                    quota_ex_day1, quota_ex_day2, quota_interactive, quota_plenary,
                    allowed_passes, is_active, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "scanner1",
                PASSWORD_HASH,
                "Gate Operations",
                0,
                "scanner",
                0, 0, 0, 0,
                json.dumps({}),
                1,
                datetime.utcnow().isoformat()
            ))
            conn.commit()
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
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_scanner_user()
