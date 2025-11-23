"""
Create All Users from Quota Spreadsheet

Creates 49 new user accounts with quotas as per spreadsheet.
Skips existing users: TDAC, SIDM, FICCI, DIO
Total organizations in spreadsheet: 50 (46 new + 4 existing)
"""
import random
import string
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
        return generate_password(length)  # Retry if conditions not met


# Organization data from spreadsheet
# Format: (username, organization, ex_day1, interactive, plenary)
# Note: ex_day2 set to 0 (not needed as interactive/plenary holders can attend exhibition day 2)
ORGANIZATIONS = [
    # Row 1-4: Strategic Business Units
    ("SB1", "SB 1", 150, 75, 100),
    ("SB2", "SB 2", 150, 75, 100),
    ("PBR", "PBR", 150, 75, 100),
    ("MBR", "MBR", 150, 75, 100),

    # Row 5: TDAC - SKIP (already exists)

    # Row 6-7: Armed Forces
    ("IndianArmy", "Indian Army", 200, 50, 50),
    ("IAF", "IAF", 150, 20, 20),

    # Row 8-10: DRDO & Others
    ("DRDO", "DRDO", 0, 20, 20),
    ("SECBM", "SEC-BM", 0, 5, 5),
    ("PRO", "PRO", 0, 4, 4),

    # Row 11-14: Media & Colleges
    ("Media1", "Media-1", 0, 25, 0),
    ("Media2", "Media-2", 0, 0, 55),
    ("VISTAR", "VISTAR", 16, 16, 16),
    ("Colleges", "Colleges", 150, 0, 150),

    # Row 15-16: SIDM, FICCI - SKIP (already exist)

    # Row 17: Coast Guard
    ("ICG", "ICG", 0, 10, 10),

    # Row 18-25: PSUs
    ("HAL", "HAL", 0, 4, 4),
    ("BEL", "BEL", 0, 4, 4),
    ("HSL", "HSL", 0, 4, 4),
    ("GSL", "GSL", 0, 4, 4),
    ("GRSE", "GRSE", 0, 4, 4),
    ("MDL", "MDL", 0, 4, 4),
    ("BDL", "BDL", 0, 4, 4),
    ("BEML", "BEML", 0, 4, 4),

    # Row 26: DIO - SKIP (already exists)

    # Row 27-31: Naval Commands
    ("NDC", "NDC", 0, 0, 10),
    ("WNC", "WNC", 0, 10, 10),
    ("SNC", "SNC", 0, 10, 10),
    ("ENC", "ENC", 0, 10, 10),
    ("ANC", "ANC", 0, 10, 10),

    # Row 32-44: Think Tanks (2 each)
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

    # Row 45-50: Special Exhibition/Interactive Only
    ("NCS", "NCS", 100, 0, 0),
    ("AFBBS", "AFBBS", 100, 0, 0),
    ("APSDK", "APS - DK", 100, 0, 0),
    ("APSSV", "APS - SV", 100, 0, 0),
    ("APSDC", "APS - DC", 0, 100, 0),
    ("Sanskriti", "Sanskriti", 0, 100, 0),
]


def create_users():
    """Create all users with quotas"""
    print("=" * 70)
    print("CREATING ALL USERS FROM SPREADSHEET")
    print("=" * 70)
    print(f"\nTotal organizations to create: {len(ORGANIZATIONS)}")
    print("\nSkipping existing users: TDAC, SIDM, FICCI, DIO")
    print("=" * 70)

    db = SessionLocal()
    credentials = []  # Store username and password for output

    try:
        created_count = 0
        skipped_count = 0

        for idx, (username, organization, ex1, interactive, plenary) in enumerate(ORGANIZATIONS, 1):
            print(f"\n{idx}. Processing: {organization} (@{username})")

            # Check if user already exists
            existing_user = db.query(User).filter(User.username == username).first()

            if existing_user:
                print(f"   ⚠️  User already exists - SKIPPING")
                skipped_count += 1
                continue

            # Generate random password
            password = generate_password()

            # Create user
            new_user = User(
                username=username,
                password_hash=hash_password(password),
                organization=organization,
                max_entries=0,  # No bulk upload for regular users
                quota_ex_day1=ex1,
                quota_ex_day2=0,  # Not needed (interactive/plenary holders can attend ex day 2)
                quota_interactive=interactive,
                quota_plenary=plenary,
                role="user",
                allowed_passes={
                    "exhibition_day1": ex1 > 0,
                    "exhibition_day2": False,  # Not needed
                    "interactive_sessions": interactive > 0,
                    "plenary": plenary > 0
                },
                is_active=True
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            credentials.append({
                'sl': idx,
                'username': username,
                'organization': organization,
                'password': password,
                'ex1': ex1,
                'interactive': interactive,
                'plenary': plenary
            })

            created_count += 1
            print(f"   ✅ Created: {username} | Password: {password}")
            print(f"      Quotas: Ex1={ex1}, Interactive={interactive}, Plenary={plenary}")

        print("\n" + "=" * 70)
        print(f"✅ CREATION COMPLETE!")
        print(f"   Created: {created_count} users")
        print(f"   Skipped: {skipped_count} users (already exist)")
        print("=" * 70)

        # Print credentials table
        print("\n\n" + "=" * 70)
        print("USER CREDENTIALS TABLE")
        print("=" * 70)
        print(f"{'Sl':<4} {'Username':<20} {'Organization':<25} {'Password':<15}")
        print("-" * 70)

        for cred in credentials:
            print(f"{cred['sl']:<4} {cred['username']:<20} {cred['organization']:<25} {cred['password']:<15}")

        print("=" * 70)
        print("\n⚠️  IMPORTANT: Save these credentials securely!")
        print("=" * 70)

        # Also save to CSV file
        import csv
        csv_path = "user_credentials.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['sl', 'username', 'organization', 'password', 'ex1', 'interactive', 'plenary'])
            writer.writeheader()
            writer.writerows(credentials)

        print(f"\n✅ Credentials also saved to: {csv_path}")

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
    create_users()
