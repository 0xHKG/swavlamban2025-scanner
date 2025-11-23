# Supabase + Streamlit Cloud Configuration Guide

## Problem: "Tenant or user not found" Error

This error occurs when connecting to Supabase from Streamlit Cloud because the **username format must include the project reference** when using the connection pooler.

---

## ✅ SOLUTION: Use Transaction Pooler with Correct Username Format

### Configuration for Streamlit Cloud Secrets

**VERIFIED WORKING Configuration (Tested Successfully):**

```toml
# Database - Supabase PostgreSQL (Transaction Pooler - IPv4 Compatible)
DB_HOST = "aws-1-ap-south-1.pooler.supabase.com"
DB_PORT = 6543
DB_NAME = "postgres"
DB_USER = "postgres.scvzcvpyvmwzigusdsjl"
DB_PASSWORD = "Ra3epL4uy45G9qTO"
```

**CRITICAL:** The project reference is `scvzcvpyvmwzigusdsjl` (note: `usdsjl` not `usdjsl`)

**Why Transaction Pooler (Port 6543)?**
- ✅ IPv4 compatible (Streamlit Cloud uses IPv4)
- ✅ Works with stateless applications like web apps
- ✅ No "Tenant or user not found" error
- ✅ Recommended by Supabase for serverless/cloud deployments

---

## How to Find Your Correct Hostname

1. Go to **Supabase Dashboard** → Your Project
2. Click **Settings** (gear icon) → **Database**
3. Scroll to **Connection String** section
4. Click **Connection Pooling** tab
5. Look for **Transaction** mode connection string
6. Copy the **exact hostname** shown there

---

## Key Differences Explained

| Setting | Session Pooler | Transaction Pooler |
|---------|----------------|-------------------|
| **Port** | 5432 | 6543 |
| **Username** | `postgres` | `postgres.scvzcvpyvmwzigusdjsl` |
| **Use Case** | Long-lived connections | Short transactions (recommended for web apps) |
| **Streamlit Cloud** | ❌ Causes "Tenant not found" | ✅ Works correctly |

---

## Steps to Fix Streamlit Cloud

### 1. Update Streamlit Secrets

Go to your Streamlit Cloud app → **Settings** → **Secrets** and use the configuration from Option 1 or 2 above.

### 2. Save Changes

Click **Save changes** button.

### 3. Reboot App

Click **Reboot app** to apply the new configuration.

### 4. Verify Success

Check the logs. You should see:
```
🗄️  Using PostgreSQL database: aws-X-ap-south-1.pooler.supabase.com
✅ Database initialized: postgresql://postgres.scvzcvpyvmwzigusdjsl:***@aws-X-ap-south-1.pooler.supabase.com:6543/postgres
```

No more "Tenant or user not found" error!

---

## Why This Works

**The Problem:**
- Supabase hosts multiple projects on the same pooler hostname/port
- The project is identified by the **username format**: `postgres.[project_ref]`
- Using just `postgres` doesn't tell Supabase which project database to connect to

**The Solution:**
- Transaction pooler (port 6543) requires `postgres.[project_ref]` username
- This uniquely identifies your project: `scvzcvpyvmwzigusdjsl`
- Supabase can now route the connection to the correct database

---

## Testing Data Persistence

After fixing the configuration:

1. **Create a test registration** in your Streamlit app
2. **Reboot the app** (Streamlit Cloud → Manage app → Reboot)
3. **Check if data persists** - the registration should still be there
4. ✅ **Success!** Data now persists forever (PostgreSQL)

Before fix: Data deleted on reboot (SQLite ephemeral storage)
After fix: Data persists forever (PostgreSQL in Supabase)

---

## Troubleshooting

### Still getting "Tenant or user not found"?

1. ✅ **Verify hostname**: Check if it's `aws-0` or `aws-1` or different
2. ✅ **Verify port**: Should be `6543` (NOT 5432)
3. ✅ **Verify username**: Should be `postgres.scvzcvpyvmwzigusdjsl` (NOT just `postgres`)
4. ✅ **Verify project ref**: Should match your Supabase project ID

### Connection timeout?

- Check if Streamlit Cloud IP is whitelisted (Supabase free tier allows all IPs by default)
- Verify password is correct (no typos)

### SSL errors?

- Our code already includes `sslmode: require` in `database.py`
- This should work automatically

---

## Reference

Based on Supabase community discussions:
- https://github.com/orgs/supabase/discussions/30107
- https://github.com/orgs/supabase/discussions/35749

**Key insight from 2023-2024 onwards:**
Supabase uses the same host/port for all projects in a region, so your database is identified by the username format `postgres.[project_ref]`.

---

Generated: 2025-10-23
