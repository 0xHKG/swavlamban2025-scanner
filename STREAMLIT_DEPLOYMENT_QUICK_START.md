# Swavlamban 2025 - Quick Deployment Guide

## Your Configuration Summary

### Database: Supabase PostgreSQL (FREE)
- **Host**: `db.scvzcvpyvmwzigusdjsl.supabase.co`
- **Port**: `5432`
- **Database**: `postgres`
- **User**: `postgres`
- **Password**: ⚠️ *Your Supabase password (from project creation)*

### Email: Gmail SMTP (FREE - 500 emails/day)
- **Email**: `Swavlamban2025@gmail.com`
- **App Password**: `pwiwmzgshilvmeon`

---

## Deployment Steps (10 minutes)

### Step 1: Push Code to GitHub

```bash
cd "/home/santosh/Desktop/Swavlamban 2025/swavlamban2025"

# Add all files
git add .

# Commit changes
git commit -m "Complete Swavlamban 2025 registration system

Features:
- Gmail SMTP integration (500 emails/day, FREE)
- PostgreSQL (Supabase) database integration
- Merged Interactive Sessions I & II into single UI element
- Fixed admin user visibility
- Complete email templates listing all passes
- Admin Panel with statistics and CSV export
- User Management with pass permissions

Ready for production deployment!

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub (you'll need to authenticate)
git push origin main
```

**Note**: If authentication fails, you may need to use a GitHub Personal Access Token.

---

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click **"New app"**
4. Configure:
   - **Repository**: `YOUR_USERNAME/swavlamban2025`
   - **Branch**: `main`
   - **Main file path**: `frontend/app.py`
5. Click **"Advanced settings"**

---

### Step 3: Configure Secrets

Copy and paste this EXACT configuration into Streamlit Cloud Secrets:

```toml
# Database - PostgreSQL (Supabase)
DB_HOST = "db.scvzcvpyvmwzigusdjsl.supabase.co"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "REPLACE_WITH_YOUR_SUPABASE_PASSWORD"

# Gmail SMTP
GMAIL_ADDRESS = "Swavlamban2025@gmail.com"
GMAIL_APP_PASSWORD = "pwiwmzgshilvmeon"
USE_GMAIL_SMTP = true

# MailBluster (Optional - not needed if using Gmail)
MAILBLUSTER_API_KEY = "f6704894-a5d2-4f7e-a4b2-61d6d30fee0b"
MAILBLUSTER_BRAND_ID = ""

# Security
JWT_SECRET_KEY = "swavlamban2025-production-secret-key-navy-tdac-2025"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Application
DEBUG = false
APP_NAME = "Swavlamban 2025"
EMAIL_SENDER = "noreply@swavlamban2025.in"
```

**⚠️ CRITICAL**: Replace `REPLACE_WITH_YOUR_SUPABASE_PASSWORD` with your actual Supabase database password!

---

### Step 4: Deploy!

1. Click **"Deploy!"**
2. Wait 2-5 minutes for deployment
3. App will be available at: `https://YOUR_APP_NAME.streamlit.app`

---

## Post-Deployment Checklist

After deployment, verify everything works:

### 1. Check Database Connection
- Look at Streamlit Cloud logs
- Should see: `🗄️ Using PostgreSQL database: db.scvzcvpyvmwzigusdjsl.supabase.co`
- **NOT**: `🗄️ Using SQLite database: ...`

### 2. Test Login
- Default admin credentials:
  - Username: `admin`
  - Password: `admin123`
  - Organization: TDAC
- **⚠️ Change password immediately after first login!**

### 3. Test Email Sending
1. Login as admin
2. Go to "Generate Passes" tab
3. Create a test entry
4. Send test email to your email address
5. Verify email arrives with QR code passes attached

### 4. Test Data Persistence
1. Create a test registration entry
2. Go to Streamlit Cloud → Reboot app
3. Login again
4. Verify test entry still exists
5. **✅ If yes**: PostgreSQL working! Data persists!
6. **❌ If no**: Check secrets configuration

### 5. Create Organization Users
1. Go to Admin Panel → Manage Users
2. Add users for each organization:
   - IIT Delhi
   - Hindustan Aeronautics Limited
   - etc.

### 6. Configure Pass Permissions
For each user, set which passes they can generate:
- ✅ Exhibition Day 1 (25 Nov)
- ✅ Exhibition Day 2 (26 Nov)
- ✅ Interactive Sessions (I & II - ONE pass)
- ✅ Plenary Session

---

## Important Notes

### Database Configuration
- **Local development**: Uses SQLite automatically (no configuration needed)
- **Streamlit Cloud**: Uses PostgreSQL (Supabase) - **MUST configure secrets**
- **Auto-detection**: App detects based on `DB_HOST` environment variable

### Email Service
- **Primary**: Gmail SMTP (500 emails/day, FREE)
- **Fallback**: MailBluster API (if configured)
- **Auto-detection**: App uses Gmail if `USE_GMAIL_SMTP = true`

### Pass Types (4 total UI elements)
1. **Exhibition Day 1** (25 Nov)
2. **Exhibition Day 2** (26 Nov)
3. **Interactive Sessions** (I & II combined - ONE pass: EP-INTERACTIVE.png)
4. **Plenary Session**

**Note**: Database stores `panel1_emerging_tech` and `panel2_idex` separately, but UI treats them as ONE pass.

---

## Troubleshooting

### Issue: App shows "Using SQLite database"
**Fix**:
1. Verify `DB_HOST` is set in Streamlit Cloud secrets
2. Ensure all 5 database variables are configured (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`)
3. Reboot app

### Issue: "Connection refused" or database error
**Fix**:
1. Verify Supabase password is correct
2. Check Supabase project is running (not paused)
3. Verify firewall allows connections from Streamlit Cloud

### Issue: Emails not sending
**Fix**:
1. Verify Gmail App Password is correct: `pwiwmzgshilvmeon`
2. Check Gmail hasn't disabled app passwords
3. Verify `USE_GMAIL_SMTP = true` in secrets

### Issue: Data lost after restart
**Fix**:
- This means PostgreSQL is NOT configured correctly
- Follow Step 3 above to add database secrets
- Reboot app after adding secrets

---

## File Structure

```
swavlamban2025/
├── frontend/
│   └── app.py                      # Main entry point (STREAMLIT RUNS THIS)
├── backend/
│   ├── app/
│   │   ├── models/                # Database models
│   │   ├── services/              # Email, QR code services
│   │   │   ├── gmail_smtp_service.py  # Gmail SMTP (FREE)
│   │   │   ├── mailbluster_service.py  # MailBluster API
│   │   │   └── email_service.py       # Auto-detection
│   │   └── core/
│   │       ├── config.py          # Configuration
│   │       ├── database.py        # PostgreSQL/SQLite auto-detection
│   │       └── security.py        # JWT auth
│   └── requirements.txt
├── requirements.txt               # Root level (Streamlit Cloud uses this)
├── runtime.txt                    # Python 3.11.6
├── .python-version               # Python 3.11
├── .streamlit/
│   └── config.toml               # Streamlit UI configuration
├── .gitignore                    # Excludes .db, .env, credentials
├── DATABASE_SETUP.md             # Database setup guide
├── DEPLOYMENT.md                 # Full deployment documentation
└── STREAMLIT_DEPLOYMENT_QUICK_START.md  # This file
```

---

## Support

### Documentation
- **Full Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Database Setup**: [DATABASE_SETUP.md](DATABASE_SETUP.md)
- **Gmail SMTP**: [GMAIL_SMTP_SETUP.md](GMAIL_SMTP_SETUP.md)
- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud

### Contact
- **Support**: niio-tdac@navy.gov.in
- **GitHub**: Create issue in repository

---

## Quick Command Reference

### Local Development
```bash
cd "/home/santosh/Desktop/Swavlamban 2025/swavlamban2025/frontend"
streamlit run app.py
```

### Access Local App
```
http://localhost:8501
```

### Kill Streamlit Process
```bash
pkill -9 streamlit
```

### View Database (SQLite - Local Only)
```bash
sqlite3 swavlamban2025.db
.tables
SELECT * FROM users;
.quit
```

---

## Deployment Status

- ✅ Code ready for deployment
- ✅ Python 3.11.6 configured
- ✅ Gmail SMTP configured (500 emails/day, FREE)
- ✅ Supabase PostgreSQL configured
- ✅ Auto-detection for local vs production
- ✅ Interactive Sessions merged (ONE pass)
- ✅ Admin user visibility fixed
- ✅ Comprehensive email templates
- ⏳ **Pending**: Push to GitHub
- ⏳ **Pending**: Deploy to Streamlit Cloud
- ⏳ **Pending**: Add Supabase password to secrets

---

**Total Cost**: $0 (completely FREE)
- Streamlit Cloud: Free tier
- Supabase: Free tier (500 MB)
- Gmail SMTP: Free (500 emails/day)

**Estimated Deployment Time**: 10-15 minutes

---

Last Updated: 2025-10-21
Ready for Production: ✅ YES
