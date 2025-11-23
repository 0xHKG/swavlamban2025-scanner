"""
Initialize database and create test data
Run this to set up the database for the first time
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import init_db, drop_db, SessionLocal
from app.core.security import hash_password
from app.models import User, Entry, CheckIn, ScannerDevice, AuditLog


def create_admin_user(db):
    """Create default admin user"""
    admin = User(
        username="admin",
        password_hash=hash_password("admin123"),  # Change in production!
        organization="TDAC",
        max_entries=999,
        role="admin",
        allowed_passes={
            "exhibition_day1": True,
            "exhibition_day2": True,
            "interactive_sessions": True,
            "interactive_sessions": True,
            "plenary": True
        },
        is_active=True
    )
    db.add(admin)
    db.commit()
    print(f"✅ Created admin user: {admin.username}")
    return admin


def create_test_users(db):
    """Create some test users for development"""
    test_users = [
        {
            "username": "iitd",
            "password": "iitd123",
            "organization": "IIT Delhi",
            "max_entries": 50,
            "allowed_passes": {
                "exhibition_day1": True,
                "exhibition_day2": True,
                "interactive_sessions": True,
                "interactive_sessions": False,
                "plenary": False
            }
        },
        {
            "username": "hal",
            "password": "hal123",
            "organization": "Hindustan Aeronautics Limited",
            "max_entries": 30,
            "allowed_passes": {
                "exhibition_day1": True,
                "exhibition_day2": True,
                "interactive_sessions": False,
                "interactive_sessions": True,
                "plenary": True
            }
        },
        {
            "username": "scanner1",
            "password": "scanner123",
            "organization": "Gate Operations",
            "max_entries": 0,
            "role": "scanner",
            "allowed_passes": {}
        }
    ]
    
    for user_data in test_users:
        role = user_data.get("role", "user")
        user = User(
            username=user_data["username"],
            password_hash=hash_password(user_data["password"]),
            organization=user_data["organization"],
            max_entries=user_data["max_entries"],
            role=role,
            allowed_passes=user_data["allowed_passes"],
            is_active=True
        )
        db.add(user)
        print(f"✅ Created {role} user: {user.username} ({user.organization})")
    
    db.commit()


def create_test_entry(db):
    """Create a sample entry for testing"""
    entry = Entry(
        username="iitd",
        name="Test Attendee",
        phone="+91-9999999999",
        email="test@iitd.ac.in",
        id_type="Aadhaar",
        id_number="1234-5678-9012",
        exhibition_day1=True,
        exhibition_day2=True,
        interactive_sessions=True,
        plenary=False
    )
    db.add(entry)
    db.commit()
    print(f"✅ Created test entry: {entry.name} (ID: {entry.id})")
    return entry


def main():
    """Initialize database with test data"""
    print("=" * 60)
    print("Swavlamban 2025 - Database Initialization")
    print("=" * 60)
    
    # Drop existing tables (BE CAREFUL IN PRODUCTION!)
    print("\n⚠️  Dropping existing database tables...")
    drop_db()
    
    # Create all tables
    print("\n📊 Creating database tables...")
    init_db()
    
    # Create test data
    print("\n👤 Creating test users...")
    db = SessionLocal()
    try:
        admin = create_admin_user(db)
        create_test_users(db)
        entry = create_test_entry(db)
        
        # Create audit log entry
        audit = AuditLog(
            username="admin",
            action="database_initialized",
            table_name="all",
            record_id=None,
            changes={"message": "Initial database setup complete"},
            ip_address="127.0.0.1"
        )
        db.add(audit)
        db.commit()
        print(f"✅ Created audit log entry")
        
        print("\n" + "=" * 60)
        print("✅ Database initialization complete!")
        print("=" * 60)
        print("\n📝 Test Credentials:")
        print("   Admin: admin / admin123")
        print("   User:  iitd / iitd123")
        print("   User:  hal / hal123")
        print("   Scanner: scanner1 / scanner123")
        print("\n⚠️  CHANGE DEFAULT PASSWORDS IN PRODUCTION!")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
