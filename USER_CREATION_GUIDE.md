# User Creation Guide

## Overview

This guide explains how to create all organization accounts for Swavlamban 2025 event using the automated script.

## Script: `create_all_users.py`

Creates 43 new organization accounts with proper quotas from the quota allocation spreadsheet.

### Organizations Created

The script creates accounts for the following categories:

#### Strategic Business Units (4)
- SB1, SB2, PBR, MBR

#### Armed Forces (2)
- Indian Army, IAF

#### DRDO & Others (3)
- DRDO, SEC-BM, PRO

#### Media & Colleges (4)
- Media-1, Media-2, VISTAR, Colleges

#### Coast Guard (1)
- ICG

#### PSUs (8)
- HAL, BEL, HSL, GSL, GRSE, MDL, BDL, BEML

#### Naval Commands (5)
- NDC, WNC, SNC, ENC, ANC

#### Think Tanks (13)
- NMF, IDSA, CAPS, CLAWS, USI, AAC, India Foundation, SPS, VIF, Bharat Shakti, ORF, SAMDeS, Delhi Policy Group

#### Special Exhibition Only (3)
- NCS, AFBBS, APS - DK

### Existing Users (NOT Created)

The script skips these 4 users that already exist:
- **TDAC** (admin)
- **SIDM**
- **FICCI**
- **DIO**

## Quota Configuration

### Quota Fields
Each user has 4 quota fields:
- `quota_ex_day1`: Exhibition Day 1 quota (25 Nov)
- `quota_ex_day2`: Exhibition Day 2 quota (26 Nov) - **Set to 0** (Interactive/Plenary holders can attend exhibition)
- `quota_interactive`: Interactive Sessions quota (26 Nov)
- `quota_plenary`: Plenary Session quota (26 Nov)

### Quota Logic
**Important**: Exhibition Day 2 quota is intentionally set to **0** for all users because:
- Interactive Sessions pass holders can attend Exhibition on Day 2
- Plenary pass holders can attend Exhibition on Day 2
- Separate Day 2 exhibition passes are not required

## Running the Script

### Prerequisites
- Database migration `migrate_add_separate_quotas.py` must be run first
- PostgreSQL database must be accessible

### Command
```bash
cd /home/santosh/Desktop/Swavlamban\ 2025/swavlamban2025
python3 create_all_users.py
```

### Output
The script will:
1. Create 43 new user accounts
2. Generate random secure passwords for each
3. Set quotas as per spreadsheet
4. Print credentials table to console
5. Save credentials to `user_credentials.csv` (gitignored)

### Security
- Passwords are randomly generated (12 characters)
- Include uppercase, lowercase, digits, and special characters
- Hashed with bcrypt before storing in database
- **Credentials CSV is gitignored** for security

## Credentials Table

After running the script, credentials are saved to:
- **Console output**: Full table printed
- **CSV file**: `user_credentials.csv` (gitignored)

### CSV Format
```csv
sl,username,organization,password,ex1,interactive,plenary
1,SB1,SB 1,<password>,150,75,100
...
```

### Important Notes
1. ⚠️ **Save credentials securely** - CSV file is not committed to git
2. ⚠️ **Share credentials via secure channel** (not email/chat)
3. ⚠️ **CSV file is temporary** - backup before deleting

## Verifying User Creation

### Check in Streamlit App
1. Restart Streamlit app
2. Go to **Admin Panel → User Management**
3. Verify all 43 users are listed
4. Check quotas are correct

### Check in Database
```bash
cd /home/santosh/Desktop/Swavlamban\ 2025/swavlamban2025
python3 -c "
from backend.app.core.database import SessionLocal
from backend.app.models.user import User

db = SessionLocal()
users = db.query(User).all()
print(f'Total users: {len(users)}')
for user in users:
    print(f'{user.organization}: Ex1={user.quota_ex_day1}, Interactive={user.quota_interactive}, Plenary={user.quota_plenary}')
db.close()
"
```

## Troubleshooting

### Error: User already exists
**Solution**: The script skips existing users automatically. This is expected for TDAC, SIDM, FICCI, DIO.

### Error: Database connection failed
**Solution**: Check `.env` file has correct `DATABASE_URL`

### Error: ImportError
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Credentials CSV not found
**Solution**: Run the script again. It generates the CSV each time.

## Next Steps After User Creation

1. ✅ **Backup credentials CSV** to secure location
2. ✅ **Share credentials** with organizations (secure channel)
3. ✅ **Test login** with sample accounts
4. ✅ **Verify quotas** in admin panel
5. ✅ **Delete credentials CSV** from server (after backup)

## Related Files

- `create_all_users.py` - User creation script
- `user_credentials.csv` - Generated credentials (gitignored)
- `migrate_add_separate_quotas.py` - Database migration (run first)
- `setup_user_quotas.py` - Set quotas for TDAC/SIDM/FICCI/DIO

## Security Best Practices

1. **Never commit credentials** to git (CSV is gitignored)
2. **Use secure channels** for sharing (not email/WhatsApp)
3. **Encourage password changes** after first login
4. **Delete CSV** after credentials are distributed
5. **Backup encrypted** credentials file separately

---

**Last Updated**: 2025-11-04
**Script Version**: 1.0
**Total Organizations**: 43 new + 4 existing = 47 total
