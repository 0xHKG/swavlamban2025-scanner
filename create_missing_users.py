"""
Create Missing Users & Reset Passwords

This script:
1. Creates 3 missing accounts (APSSV, APSDC, Sanskriti)
2. Optionally resets passwords for existing 43 accounts
3. Generates credentials document for all 46 accounts (excluding TDAC, SIDM, FICCI, DIO)
"""
import random
import string
import csv
from sqlalchemy import text
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import hash_password


def generate_password(length=12):
    """Generate a random password"""
    characters = string.ascii_letters + string.digits + "!@#$%"
    password = ''.join(random.choice(characters) for i in range(length))
    # Ensure it has at least one uppercase, lowercase, digit, and special char
    if (any(c.isupper() for c in password) and
        any(c.islower() for c in password) and
        any(c.isdigit() for c in password) and
        any(c in "!@#$%" for c in password)):
        return password
    else:
        return generate_password(length)


# Missing users to create
MISSING_USERS = [
    ("APSSV", "APS - SV", 100, 0, 0),
    ("APSDC", "APS - DC", 0, 100, 0),
    ("Sanskriti", "Sanskriti", 0, 100, 0),
]

# All 46 accounts (excluding TDAC, SIDM, FICCI, DIO)
ALL_46_ACCOUNTS = [
    ("SB1", "SB 1", 150, 75, 100),
    ("SB2", "SB 2", 150, 75, 100),
    ("PBR", "PBR", 150, 75, 100),
    ("MBR", "MBR", 150, 75, 100),
    ("IndianArmy", "Indian Army", 200, 50, 50),
    ("IAF", "IAF", 150, 20, 20),
    ("DRDO", "DRDO", 0, 20, 20),
    ("SECBM", "SEC-BM", 0, 5, 5),
    ("PRO", "PRO", 0, 4, 4),
    ("Media1", "Media-1", 0, 25, 0),
    ("Media2", "Media-2", 0, 0, 55),
    ("VISTAR", "VISTAR", 16, 16, 16),
    ("Colleges", "Colleges", 150, 0, 150),
    ("ICG", "ICG", 0, 10, 10),
    ("HAL", "HAL", 0, 4, 4),
    ("BEL", "BEL", 0, 4, 4),
    ("HSL", "HSL", 0, 4, 4),
    ("GSL", "GSL", 0, 4, 4),
    ("GRSE", "GRSE", 0, 4, 4),
    ("MDL", "MDL", 0, 4, 4),
    ("BDL", "BDL", 0, 4, 4),
    ("BEML", "BEML", 0, 4, 4),
    ("NDC", "NDC", 0, 0, 10),
    ("WNC", "WNC", 0, 10, 10),
    ("SNC", "SNC", 0, 10, 10),
    ("ENC", "ENC", 0, 10, 10),
    ("ANC", "ANC", 0, 10, 10),
    ("NMF", "NMF", 0, 2, 2),
    ("IDSA", "IDSA", 0, 2, 2),
    ("CAPS", "CAPS", 0, 2, 2),
    ("CLAWS", "CLAWS", 0, 2, 2),
    ("USI", "USI", 0, 2, 2),
    ("AAC", "AAC", 0, 2, 2),
    ("IndiaFoundation", "India Foundation", 0, 2, 2),
    ("SPS", "SPS", 0, 2, 2),
    ("VIF", "VIF", 0, 2, 2),
    ("BharatShakti", "Bharat Shakti", 0, 2, 2),
    ("ORF", "ORF", 0, 2, 2),
    ("SAMDeS", "SAMDeS", 0, 2, 2),
    ("DelhiPolicyGroup", "Delhi Policy Group", 0, 2, 2),
    ("NCS", "NCS", 100, 0, 0),
    ("AFBBS", "AFBBS", 100, 0, 0),
    ("APSDK", "APS - DK", 100, 0, 0),
    ("APSSV", "APS - SV", 100, 0, 0),
    ("APSDC", "APS - DC", 0, 100, 0),
    ("Sanskriti", "Sanskriti", 0, 100, 0),
]


def create_missing_and_reset():
    """Create missing users and reset passwords for existing ones"""
    print("=" * 80)
    print("CREATE MISSING USERS & RESET PASSWORDS FOR ALL 46 ACCOUNTS")
    print("=" * 80)
    print(f"\nThis will:")
    print("  1. Create 3 missing accounts (APSSV, APSDC, Sanskriti)")
    print("  2. Reset passwords for 43 existing accounts")
    print("  3. Generate credentials document for all 46 accounts")
    print(f"\nExcluding: TDAC, SIDM, FICCI, DIO (4 accounts)")
    print("=" * 80)

    response = input("\nProceed? (yes/no): ").strip().lower()
    if response != 'yes':
        print("❌ Aborted by user")
        return False

    db = SessionLocal()
    credentials = []

    try:
        created_count = 0
        reset_count = 0

        for idx, (username, organization, ex1, interactive, plenary) in enumerate(ALL_46_ACCOUNTS, 1):
            print(f"\n{idx}. Processing: {organization} (@{username})")

            # Check if user exists
            existing_user = db.query(User).filter(User.username == username).first()

            # Generate password
            password = generate_password()

            if existing_user:
                # Reset password
                existing_user.password_hash = hash_password(password)
                db.commit()
                reset_count += 1
                print(f"   🔄 Password RESET: {username} | New Password: {password}")
            else:
                # Create new user
                new_user = User(
                    username=username,
                    password_hash=hash_password(password),
                    organization=organization,
                    max_entries=0,
                    quota_ex_day1=ex1,
                    quota_ex_day2=0,
                    quota_interactive=interactive,
                    quota_plenary=plenary,
                    role="user",
                    allowed_passes={
                        "exhibition_day1": ex1 > 0,
                        "exhibition_day2": False,
                        "interactive_sessions": interactive > 0,
                        "plenary": plenary > 0
                    },
                    is_active=True
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                created_count += 1
                print(f"   ✅ CREATED: {username} | Password: {password}")

            # Store credentials
            credentials.append({
                'sl': idx,
                'username': username,
                'organization': organization,
                'password': password,
                'ex1': ex1,
                'interactive': interactive,
                'plenary': plenary
            })

            print(f"      Quotas: Ex1={ex1}, Interactive={interactive}, Plenary={plenary}")

        print("\n" + "=" * 80)
        print(f"✅ OPERATION COMPLETE!")
        print(f"   Created: {created_count} new accounts")
        print(f"   Reset: {reset_count} existing accounts")
        print(f"   Total: {len(credentials)} accounts processed")
        print("=" * 80)

        # Save credentials to CSV
        csv_path = "user_credentials_all_46.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['sl', 'username', 'organization', 'password', 'ex1', 'interactive', 'plenary'])
            writer.writeheader()
            writer.writerows(credentials)

        print(f"\n✅ Credentials saved to: {csv_path}")

        # Print credentials table
        print("\n\n" + "=" * 80)
        print("COMPLETE CREDENTIALS TABLE - ALL 46 ACCOUNTS")
        print("=" * 80)
        print(f"{'Sl':<4} {'Username':<22} {'Organization':<25} {'Password':<15}")
        print("-" * 80)

        for cred in credentials:
            print(f"{cred['sl']:<4} {cred['username']:<22} {cred['organization']:<25} {cred['password']:<15}")

        print("=" * 80)
        print("\n⚠️  IMPORTANT: Share these credentials securely with organizations!")
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
    create_missing_and_reset()
