"""
Database Migration Script
Adds is_exhibitor_pass field to entries table

Run this script to update the database schema:
    python run_migration.py
"""

from backend.app.core.database import engine
from sqlalchemy import text

def run_migration():
    """Add is_exhibitor_pass column to entries table"""

    print("Starting database migration...")
    print("Adding is_exhibitor_pass column to entries table...\n")

    with engine.connect() as conn:
        try:
            # Add the new column
            conn.execute(text("""
                ALTER TABLE entries
                ADD COLUMN IF NOT EXISTS is_exhibitor_pass BOOLEAN DEFAULT FALSE NOT NULL;
            """))
            conn.commit()
            print("✅ Column is_exhibitor_pass added successfully!")

            # Set all existing entries to False (they are visitors)
            result = conn.execute(text("""
                UPDATE entries
                SET is_exhibitor_pass = FALSE
                WHERE is_exhibitor_pass IS NULL OR is_exhibitor_pass = FALSE;
            """))
            conn.commit()
            print(f"✅ Updated {result.rowcount} existing entries to is_exhibitor_pass=False")

            # Verification
            result = conn.execute(text("""
                SELECT
                    COUNT(*) as total_entries,
                    SUM(CASE WHEN is_exhibitor_pass = TRUE THEN 1 ELSE 0 END) as exhibitors,
                    SUM(CASE WHEN is_exhibitor_pass = FALSE THEN 1 ELSE 0 END) as visitors
                FROM entries;
            """))
            row = result.fetchone()

            print(f"\n📊 Database Status:")
            print(f"   Total entries: {row[0]}")
            print(f"   Exhibitors: {row[1]}")
            print(f"   Visitors: {row[2]}")

            print("\n✅ Migration completed successfully!")
            print("   You can now restart your Streamlit app.")

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    run_migration()
