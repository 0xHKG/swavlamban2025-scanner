#!/usr/bin/env python3
"""
Complete setup script for Scanner PWA testing
- Initializes database with all tables
- Creates test scanner user
- Creates test entry for QR scanning
"""
import sqlite3
from datetime import datetime
import json
import random
import string

DB_PATH = "/home/user/swavlamban2025/swavlamban2025.db"

# Pre-computed bcrypt hash for "scanner123"
SCANNER_PASSWORD_HASH = "$2b$12$LKaGPj7QQYHJvZ9X1.vvnO8wYc3YqN6yJxH0vP6eJ5X7.aKZ5YH2m"

# Pre-computed bcrypt hash for "admin123"
ADMIN_PASSWORD_HASH = "$2b$12$K8X5YqZ9X1.vvnO8wYc3YqN6yJxH0vP6eJ5X7.aKZ5YH2mLKaGPj7Q"

def create_tables(cursor):
    """Create all database tables"""

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            organization TEXT NOT NULL,
            max_entries INTEGER NOT NULL DEFAULT 0,
            role TEXT DEFAULT 'user',
            quota_ex_day1 INTEGER DEFAULT 0,
            quota_ex_day2 INTEGER DEFAULT 0,
            quota_interactive INTEGER DEFAULT 0,
            quota_plenary INTEGER DEFAULT 0,
            allowed_passes TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)

    # Entries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            id_type TEXT NOT NULL,
            id_number TEXT NOT NULL UNIQUE,
            photo_url TEXT,
            qr_signature TEXT,
            organization TEXT NOT NULL,

            exhibition_day1 INTEGER DEFAULT 0,
            exhibition_day2 INTEGER DEFAULT 0,
            interactive_sessions INTEGER DEFAULT 0,
            plenary INTEGER DEFAULT 0,
            is_exhibitor INTEGER DEFAULT 0,

            pass_generated_exhibition_day1 INTEGER DEFAULT 0,
            pass_generated_exhibition_day2 INTEGER DEFAULT 0,
            pass_generated_interactive_sessions INTEGER DEFAULT 0,
            pass_generated_plenary INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)

    # Check-ins table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS check_ins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL,
            session_type TEXT NOT NULL,
            gate_number TEXT NOT NULL,
            gate_location TEXT NOT NULL,
            check_in_time TIMESTAMP NOT NULL,
            scanner_device_id TEXT,
            scanner_operator TEXT,
            qr_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (entry_id) REFERENCES entries(id)
        )
    """)

    # Scanner devices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scanner_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE NOT NULL,
            operator_username TEXT,
            gate_number TEXT,
            is_active INTEGER DEFAULT 1,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def main():
    """Main setup function"""
    print("🚀 Scanner PWA Test Setup")
    print("=" * 50)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Step 1: Create tables
        print("\n1️⃣  Creating database tables...")
        create_tables(cursor)
        print("   ✅ Tables created")

        # Step 2: Create scanner user
        print("\n2️⃣  Creating scanner user...")
        cursor.execute("SELECT username FROM users WHERE username = ?", ("scanner1",))
        if cursor.fetchone():
            print("   ⚠️  Scanner user already exists")
        else:
            cursor.execute("""
                INSERT INTO users (
                    username, password_hash, organization, max_entries, role,
                    quota_ex_day1, quota_ex_day2, quota_interactive, quota_plenary,
                    allowed_passes, is_active, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "scanner1", SCANNER_PASSWORD_HASH, "Gate Operations", 0, "scanner",
                0, 0, 0, 0, json.dumps({}), 1, datetime.utcnow().isoformat()
            ))
            print("   ✅ Scanner user created")

        # Step 3: Create test admin user (if doesn't exist)
        print("\n3️⃣  Checking admin user...")
        cursor.execute("SELECT username FROM users WHERE username = ?", ("admin",))
        if cursor.fetchone():
            print("   ✅ Admin user already exists")
        else:
            cursor.execute("""
                INSERT INTO users (
                    username, password_hash, organization, max_entries, role,
                    quota_ex_day1, quota_ex_day2, quota_interactive, quota_plenary,
                    allowed_passes, is_active, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "admin", ADMIN_PASSWORD_HASH, "TDAC", 999, "admin",
                999, 999, 999, 999,
                json.dumps({
                    "exhibition_day1": True,
                    "exhibition_day2": True,
                    "interactive_sessions": True,
                    "plenary": True
                }),
                1, datetime.utcnow().isoformat()
            ))
            print("   ✅ Admin user created")

        # Step 4: Create test entry for QR scanning
        print("\n4️⃣  Creating test entry...")
        test_signature = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        cursor.execute("SELECT id FROM entries WHERE email = ?", ("test@example.com",))
        existing_entry = cursor.fetchone()

        if existing_entry:
            entry_id = existing_entry[0]
            print(f"   ⚠️  Test entry already exists (ID: {entry_id})")
        else:
            cursor.execute("""
                INSERT INTO entries (
                    username, name, phone, email, id_type, id_number,
                    qr_signature, organization,
                    exhibition_day1, exhibition_day2, interactive_sessions, plenary,
                    pass_generated_exhibition_day1, pass_generated_exhibition_day2,
                    pass_generated_interactive_sessions, pass_generated_plenary,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "admin", "Test User", "9876543210", "test@example.com",
                "Aadhaar", "1234-5678-9012", test_signature, "Test Organization",
                1, 1, 1, 1,  # All passes allocated
                1, 1, 1, 1,  # All passes generated
                datetime.utcnow().isoformat(), datetime.utcnow().isoformat()
            ))
            entry_id = cursor.lastrowid
            print(f"   ✅ Test entry created (ID: {entry_id})")

        conn.commit()

        # Print summary
        print("\n" + "=" * 50)
        print("✅ Setup Complete!")
        print("=" * 50)

        print("\n📋 Scanner Login Credentials:")
        print("   Username: scanner1")
        print("   Password: scanner123")
        print("   Role: scanner")

        print("\n📋 Admin Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Role: admin")

        print("\n🎯 Test QR Codes:")
        print(f"   Exhibition Day 1: {entry_id}:exhibition_day1:{test_signature}")
        print(f"   Exhibition Day 2: {entry_id}:exhibition_day2:{test_signature}")
        print(f"   Interactive Sessions: {entry_id}:interactive_sessions:{test_signature}")
        print(f"   Plenary: {entry_id}:plenary:{test_signature}")

        print("\n🚀 Next Steps:")
        print("   1. Start backend:  python3 -m backend.app.main")
        print("   2. Frontend running at: http://localhost:3000")
        print("   3. Login with scanner1/scanner123")
        print("   4. Select a gate and start scanning!")

        print("\n💡 Generate QR codes at:")
        print("   https://www.qr-code-generator.com")
        print(f"   Use text: {entry_id}:exhibition_day1:{test_signature}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
