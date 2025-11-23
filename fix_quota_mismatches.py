"""
Fix Quota Mismatches in Database

Updates quotas for users that don't match the spreadsheet:
- IndianArmy: Interactive 60 → 50
- DRDO: Interactive 5 → 20, Plenary 5 → 20
- Media2: Plenary 0 → 55
"""
from backend.app.core.database import SessionLocal
from backend.app.models.user import User

# Quota corrections
QUOTA_FIXES = [
    ("IndianArmy", {"quota_interactive": 50}),  # Was 60, should be 50
    ("DRDO", {"quota_interactive": 20, "quota_plenary": 20}),  # Was 5/5, should be 20/20
    ("Media2", {"quota_plenary": 55}),  # Was 0, should be 55
]


def fix_quotas():
    """Fix quota mismatches in database"""
    print("=" * 80)
    print("FIXING QUOTA MISMATCHES IN DATABASE")
    print("=" * 80)

    db = SessionLocal()

    try:
        fixed_count = 0

        for username, updates in QUOTA_FIXES:
            print(f"\nFixing {username}:")

            user = db.query(User).filter(User.username == username).first()

            if not user:
                print(f"   ❌ User not found: {username}")
                continue

            # Show before values
            print(f"   Before: Ex1={user.quota_ex_day1}, Interactive={user.quota_interactive}, Plenary={user.quota_plenary}")

            # Apply updates
            for field, value in updates.items():
                setattr(user, field, value)

            db.commit()
            db.refresh(user)

            # Show after values
            print(f"   After:  Ex1={user.quota_ex_day1}, Interactive={user.quota_interactive}, Plenary={user.quota_plenary}")
            print(f"   ✅ Fixed")

            fixed_count += 1

        print("\n" + "=" * 80)
        print(f"✅ COMPLETE! Fixed {fixed_count} users")
        print("=" * 80)

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
    fix_quotas()
