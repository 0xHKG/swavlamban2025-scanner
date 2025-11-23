"""
Database Migration: Add Separate Quotas for Each Pass Type

This migration adds individual quota columns for each pass type:
- quota_ex_day1: Quota for Exhibition Day 1 passes
- quota_ex_day2: Quota for Exhibition Day 2 passes
- quota_interactive: Quota for Interactive Sessions passes
- quota_plenary: Quota for Plenary Session passes

This allows organizations to have different quotas for different pass types.
For example: 5 Ex Day 1, 1 Ex Day 2, 13 Interactive, 15 Plenary
"""

from sqlalchemy import create_engine, text
from backend.app.core.database import engine

def run_migration():
    """Add separate quota columns to users table"""
    print("Starting database migration: Add separate pass quotas...")

    with engine.connect() as conn:
        try:
            # Add the new quota columns with default value 0
            print("Adding quota_ex_day1 column...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS quota_ex_day1 INTEGER DEFAULT 0 NOT NULL;
            """))
            conn.commit()

            print("Adding quota_ex_day2 column...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS quota_ex_day2 INTEGER DEFAULT 0 NOT NULL;
            """))
            conn.commit()

            print("Adding quota_interactive column...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS quota_interactive INTEGER DEFAULT 0 NOT NULL;
            """))
            conn.commit()

            print("Adding quota_plenary column...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS quota_plenary INTEGER DEFAULT 0 NOT NULL;
            """))
            conn.commit()

            # Initialize existing users with 0 for all new quotas
            print("Initializing existing users with 0 quotas...")
            result = conn.execute(text("""
                UPDATE users
                SET quota_ex_day1 = 0,
                    quota_ex_day2 = 0,
                    quota_interactive = 0,
                    quota_plenary = 0
                WHERE quota_ex_day1 IS NULL
                   OR quota_ex_day2 IS NULL
                   OR quota_interactive IS NULL
                   OR quota_plenary IS NULL;
            """))
            conn.commit()
            print(f"✅ Initialized {result.rowcount} existing users")

            print("✅ Migration completed successfully!")
            print("\n📝 NEXT STEPS:")
            print("1. Restart your Streamlit app")
            print("2. Go to Admin Panel → User Management")
            print("3. Edit each organization to set their pass quotas")
            print("4. Users will now have separate quotas for each pass type")
            return True

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            conn.rollback()
            return False

if __name__ == "__main__":
    run_migration()
