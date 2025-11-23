# Database Setup Guide - Swavlamban 2025

## ⚠️ CRITICAL: Data Persistence Issue

### The Problem with SQLite on Streamlit Cloud:

**Streamlit Cloud uses EPHEMERAL file system:**
- ❌ SQLite database file is **DELETED on every app restart**
- ❌ All registrations, passes, and data are **LOST**
- ❌ **NOT suitable for production use**

### When Data is Lost:
- When you update code and redeploy
- When Streamlit Cloud restarts your app
- When app crashes or reboots
- When you change any settings

**Result**: Complete data loss every time!

---

## ✅ Solution: External PostgreSQL Database

Use a **persistent PostgreSQL database** hosted externally.

---

## Option 1: Supabase (Recommended - FREE)

### Why Supabase?
- ✅ **500 MB free tier** (enough for 10,000+ attendees)
- ✅ **Unlimited rows**
- ✅ **Automatic backups**
- ✅ **Real-time dashboard**
- ✅ **No credit card required**
- ✅ **Data persists forever**

### Setup Steps (5 minutes):

#### Step 1: Create Supabase Account
1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub (or email)

#### Step 2: Create New Project
1. Click "New Project"
2. **Name**: `swavlamban2025`
3. **Database Password**: Create strong password (save it!)
4. **Region**: Select closest to India (e.g., Singapore, Mumbai if available)
5. Click "Create new project"
6. Wait 1-2 minutes for setup

#### Step 3: Get Connection Details
1. Go to **Settings** (gear icon) → **Database**
2. Scroll to "Connection string"
3. Select **"URI"** tab
4. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.abc123xyz.supabase.co:5432/postgres
   ```

#### Step 4: Update Streamlit Cloud Secrets
1. Go to Streamlit Cloud → Your App → Settings → Secrets
2. Add these variables (YOUR ACTUAL CONFIGURATION):

```toml
# Database - PostgreSQL (Supabase)
# Your Supabase connection: db.scvzcvpyvmwzigusdjsl.supabase.co
DB_HOST = "db.scvzcvpyvmwzigusdjsl.supabase.co"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "your-supabase-database-password-here"

# Gmail SMTP
GMAIL_ADDRESS = "Swavlamban2025@gmail.com"
GMAIL_APP_PASSWORD = "pwiwmzgshilvmeon"
USE_GMAIL_SMTP = true

# Security
JWT_SECRET_KEY = "your-production-secret-key-change-this"
DEBUG = false
```

**IMPORTANT**: Replace `your-supabase-database-password-here` with your actual Supabase database password.

#### Step 5: Restart Streamlit App
- Click "Reboot app" in Streamlit Cloud
- App will now use PostgreSQL
- Data will persist across restarts!

---

## Option 2: ElephantSQL (FREE Alternative)

### Setup:
1. Go to https://www.elephantsql.com
2. Sign up free
3. Create new instance (Tiny Turtle - FREE)
4. Copy connection URL
5. Parse URL to get:
   - Host
   - Port (usually 5432)
   - Database name
   - Username
   - Password
6. Add to Streamlit secrets (same as above)

**Free Tier**: 20 MB (good for ~2,000 attendees)

---

## Option 3: Neon.tech (Modern Alternative)

### Setup:
1. Go to https://neon.tech
2. Sign up with GitHub
3. Create project
4. Get connection string
5. Add to Streamlit secrets

**Free Tier**: 500 MB + 3 GB storage

---

## Local Development Setup

### For Local Testing (Your Computer):

**Uses SQLite automatically** - no configuration needed!

```bash
# Just run the app
cd "/home/santosh/Desktop/Swavlamban 2025/swavlamban2025/frontend"
streamlit run app.py
```

Database file: `swavlamban2025.db` in project root

---

## How Auto-Detection Works

The app automatically detects which database to use:

### Local Development:
- **No** `DB_HOST` environment variable
- **Uses**: SQLite (`swavlamban2025.db`)
- **Data**: Stored in local file

### Streamlit Cloud (Production):
- **Has** `DB_HOST` in secrets
- **Uses**: PostgreSQL (Supabase/ElephantSQL/Neon)
- **Data**: Stored in external database (persistent!)

---

## Database Migration (First Deployment)

### After Setting Up PostgreSQL:

#### 1. Initialize Tables
App will auto-create tables on first run:
- `users` - User accounts
- `entries` - Attendee registrations
- `check_ins` - Gate check-ins
- `scanner_devices` - Scanner devices
- `audit_log` - Audit trail

#### 2. Create Admin User
Login functionality will auto-create admin if not exists, OR use Admin Panel → Manage Users

#### 3. Import Existing Data (If Any)
If you have existing SQLite data:

```python
# Export from SQLite
import sqlite3
import pandas as pd

conn = sqlite3.connect('swavlamban2025.db')
users = pd.read_sql('SELECT * FROM users', conn)
entries = pd.read_sql('SELECT * FROM entries', conn)

# Save to CSV
users.to_csv('users_backup.csv', index=False)
entries.to_csv('entries_backup.csv', index=False)
```

Then import via Admin Panel (CSV export/import feature)

---

## Backup Strategy

### Automatic Backups:
- **Supabase**: Automatic daily backups (7 days retention on free tier)
- **ElephantSQL**: Automatic backups
- **Neon**: Point-in-time recovery

### Manual Backups:
Use Admin Panel → Download Organization Report (CSV)
- Exports all registrations
- Download before major changes
- Keep offline copies

---

## Testing Database Connection

### Method 1: Check Streamlit Logs
After deployment, check app logs:
- Should see: `🗄️ Using PostgreSQL database: db.xyz.supabase.co`
- NOT: `🗄️ Using SQLite database: ...`

### Method 2: Create Test Entry
1. Create a test registration
2. Restart app (reboot in Streamlit Cloud)
3. Check if test entry still exists
4. If yes → PostgreSQL working! ✅
5. If no → Still using SQLite (ephemeral) ❌

---

## Troubleshooting

### Issue: "Connection refused" or Database Error

**Cause**: PostgreSQL credentials incorrect

**Fix**:
1. Verify credentials in Supabase/ElephantSQL dashboard
2. Check firewall allows connection
3. Ensure secrets in Streamlit Cloud are correct
4. Restart Streamlit app

### Issue: App Still Using SQLite

**Cause**: `DB_HOST` not set in Streamlit secrets

**Fix**:
1. Add all database variables to Streamlit Cloud → Secrets
2. Ensure variable names match exactly: `DB_HOST`, `DB_PORT`, etc.
3. Restart app

### Issue: Data Lost After Restart

**Cause**: Still using SQLite (ephemeral)

**Fix**: Follow Supabase setup above to switch to PostgreSQL

---

## Cost Comparison

| Provider | Free Tier | Max Attendees | Persistence |
|----------|-----------|---------------|-------------|
| **SQLite (Streamlit)** | ❌ | N/A | ❌ Ephemeral |
| **Supabase** | ✅ 500 MB | ~10,000+ | ✅ Forever |
| **ElephantSQL** | ✅ 20 MB | ~2,000 | ✅ Forever |
| **Neon** | ✅ 500 MB | ~10,000+ | ✅ Forever |

---

## Recommendation

**For Swavlamban 2025 Event:**

Use **Supabase** because:
- ✅ Best free tier (500 MB)
- ✅ Easy setup (5 minutes)
- ✅ Automatic backups
- ✅ Indian servers available (low latency)
- ✅ Real-time dashboard to view data
- ✅ No credit card needed
- ✅ Data persists forever

**Total Cost**: $0 (completely free)

---

## Quick Setup Checklist

- [ ] Create Supabase account
- [ ] Create new project
- [ ] Copy database credentials
- [ ] Add credentials to Streamlit Cloud secrets
- [ ] Restart Streamlit app
- [ ] Verify PostgreSQL is being used (check logs)
- [ ] Create test registration
- [ ] Restart app again
- [ ] Verify test data still exists
- [ ] ✅ Ready for production!

---

## Summary

**Current Setup (Local)**:
- Database: SQLite
- File: `swavlamban2025.db`
- Persistence: ✅ Local file (persists)

**Streamlit Cloud (Without PostgreSQL)**:
- Database: SQLite
- File: Temporary (in-memory)
- Persistence: ❌ **DELETED ON RESTART**

**Streamlit Cloud (With PostgreSQL)**:
- Database: PostgreSQL (Supabase)
- Location: External server
- Persistence: ✅ **FOREVER**

**Action Required**: Set up PostgreSQL before production deployment!

---

Last Updated: 2025-10-21
Estimated Setup Time: 5-10 minutes
Cost: $0 (Free tier)
