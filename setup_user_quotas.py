"""
Setup User Quotas for Organizations

Sets up quotas for:
- TDAC: 999 total, 999 for each pass
- SIDM: 100 total, 100 for each pass
- FICCI: 100 total, 100 for each pass
- DoI: 100 total, 100 for each pass
"""

from sqlalchemy import text
from backend.app.core.database import engine
from backend.app.models.user import User
from backend.app.core.database import SessionLocal

def setup_quotas():
    """Setup quotas for specified organizations"""
    print("Setting up user quotas...")

    db = SessionLocal()

    try:
        # TDAC: 999 total, 999 for each pass
        print("\n1. Updating TDAC...")
        tdac = db.query(User).filter(User.username == "admin").first()
        if tdac:
            tdac.max_entries = 999
            tdac.quota_ex_day1 = 999
            tdac.quota_ex_day2 = 999
            tdac.quota_interactive = 999
            tdac.quota_plenary = 999
            # Enable all pass permissions
            tdac.allowed_passes = {
                "exhibition_day1": True,
                "exhibition_day2": True,
                "interactive_sessions": True,
                "plenary": True
            }
            print(f"   ✅ TDAC updated: Max Entries={tdac.max_entries}, Quotas=999 each")
        else:
            print("   ❌ TDAC (admin) user not found!")

        # SIDM: 100 total, 100 for each pass
        print("\n2. Updating/Creating SIDM...")
        sidm = db.query(User).filter(User.username == "SIDM").first()
        if sidm:
            sidm.max_entries = 100
            sidm.quota_ex_day1 = 100
            sidm.quota_ex_day2 = 100
            sidm.quota_interactive = 100
            sidm.quota_plenary = 100
            sidm.allowed_passes = {
                "exhibition_day1": True,
                "exhibition_day2": True,
                "interactive_sessions": True,
                "plenary": True
            }
            print(f"   ✅ SIDM updated: Max Entries={sidm.max_entries}, Quotas=100 each")
        else:
            print("   ℹ️  SIDM user not found in database")

        # FICCI: 100 total, 100 for each pass
        print("\n3. Updating/Creating FICCI...")
        ficci = db.query(User).filter(User.username == "FICCI").first()
        if ficci:
            ficci.max_entries = 100
            ficci.quota_ex_day1 = 100
            ficci.quota_ex_day2 = 100
            ficci.quota_interactive = 100
            ficci.quota_plenary = 100
            ficci.allowed_passes = {
                "exhibition_day1": True,
                "exhibition_day2": True,
                "interactive_sessions": True,
                "plenary": True
            }
            print(f"   ✅ FICCI updated: Max Entries={ficci.max_entries}, Quotas=100 each")
        else:
            print("   ℹ️  FICCI user not found in database")

        # DoI: 100 total, 100 for each pass
        print("\n4. Updating/Creating DoI...")
        doi = db.query(User).filter(User.username == "DIO").first()
        if not doi:
            doi = db.query(User).filter(User.username == "DOI").first()
        if not doi:
            doi = db.query(User).filter(User.username == "dio").first()
        if not doi:
            doi = db.query(User).filter(User.username == "doi").first()

        if doi:
            doi.max_entries = 100
            doi.quota_ex_day1 = 100
            doi.quota_ex_day2 = 100
            doi.quota_interactive = 100
            doi.quota_plenary = 100
            doi.allowed_passes = {
                "exhibition_day1": True,
                "exhibition_day2": True,
                "interactive_sessions": True,
                "plenary": True
            }
            print(f"   ✅ DoI updated: Max Entries={doi.max_entries}, Quotas=100 each")
        else:
            print("   ℹ️  DoI user not found in database")

        # Commit all changes
        db.commit()
        print("\n" + "="*60)
        print("✅ All quotas updated successfully!")
        print("="*60)

        # Show summary
        print("\n📊 Summary of Users:")
        print("-" * 60)
        all_users = db.query(User).all()
        for user in all_users:
            print(f"\n{user.organization} (@{user.username}):")
            print(f"  Max Entries: {user.max_entries}")
            print(f"  Ex Day 1: {getattr(user, 'quota_ex_day1', 0)}")
            print(f"  Ex Day 2: {getattr(user, 'quota_ex_day2', 0)}")
            print(f"  Interactive: {getattr(user, 'quota_interactive', 0)}")
            print(f"  Plenary: {getattr(user, 'quota_plenary', 0)}")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return False

    finally:
        db.close()

if __name__ == "__main__":
    setup_quotas()
