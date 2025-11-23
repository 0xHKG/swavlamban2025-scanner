# Swavlamban 2025 - Streamlit Cloud Deployment Guide

## Prerequisites

- GitHub account
- Streamlit Cloud account (https://streamlit.io/cloud)
- Gmail account with App Password configured

---

## Step 1: Push Code to GitHub

### 1.1 Initialize Git Repository (if not already done)
```bash
cd "/home/santosh/Desktop/Swavlamban 2025/swavlamban2025"
git init
git add .
git commit -m "Initial commit - Swavlamban 2025 Registration System"
```

### 1.2 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `swavlamban2025`
3. Description: "Indian Navy Swavlamban 2025 - Registration & Pass Management System"
4. Visibility: **Private** (contains sensitive event data)
5. Click "Create repository"

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/swavlamban2025.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Streamlit Cloud

### 2.1 Sign in to Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Sign in with GitHub

### 2.2 Create New App
1. Click "New app"
2. **Repository**: Select `YOUR_USERNAME/swavlamban2025`
3. **Branch**: `main`
4. **Main file path**: `frontend/app.py`
5. **Python version**: Will use `runtime.txt` (Python 3.11.6)

### 2.3 Configure Secrets
Click "Advanced settings" → "Secrets" and add:

```toml
# Database - PostgreSQL (Supabase) ⚠️ REQUIRED FOR PRODUCTION
DB_HOST = "db.scvzcvpyvmwzigusdjsl.supabase.co"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "your-supabase-database-password-here"

# Gmail SMTP Configuration
GMAIL_ADDRESS = "Swavlamban2025@gmail.com"
GMAIL_APP_PASSWORD = "pwiwmzgshilvmeon"
USE_GMAIL_SMTP = true

# MailBluster (Optional)
MAILBLUSTER_API_KEY = "f6704894-a5d2-4f7e-a4b2-61d6d30fee0b"
MAILBLUSTER_BRAND_ID = ""

# Security
JWT_SECRET_KEY = "your-production-secret-key-change-this-abc123xyz789"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Application
DEBUG = false
APP_NAME = "Swavlamban 2025"
EMAIL_SENDER = "noreply@swavlamban2025.in"
```

**⚠️ CRITICAL**: Replace `your-supabase-database-password-here` with your actual Supabase database password before deploying!

### 2.4 Deploy
Click "Deploy!" and wait for deployment to complete (~2-5 minutes)

---

## Step 3: Initialize Database

After deployment, the app will automatically:
1. Create SQLite database file
2. Initialize tables
3. Create default admin user (if using init_db script)

### Default Admin Credentials:
- **Username**: `admin`
- **Password**: `admin123`
- **Organization**: TDAC

**⚠️ IMPORTANT**: Change the admin password immediately after first login!

---

## Step 4: Post-Deployment Configuration

### 4.1 Test Email Sending
1. Login as admin
2. Go to "Generate Passes" tab
3. Create a test entry
4. Send test email to verify Gmail SMTP works

### 4.2 Create Organization Users
1. Go to Admin Panel → Manage Users
2. Add users for each organization:
   - IIT Delhi
   - Hindustan Aeronautics Limited
   - etc.

### 4.3 Configure Pass Permissions
For each user, set which pass types they can generate:
- Exhibition Day 1
- Exhibition Day 2
- Interactive Sessions (I & II)
- Plenary Session

---

## Important Files for Deployment

### Configuration Files:
- **`requirements.txt`** - Python dependencies (root level for Streamlit Cloud)
- **`runtime.txt`** - Python version (3.11.6)
- **`.python-version`** - Python version for local development
- **`.streamlit/config.toml`** - Streamlit UI configuration

### Application Structure:
```
swavlamban2025/
├── frontend/
│   ├── app.py                 # Main Streamlit app (entry point)
│   └── requirements.txt       # Frontend-specific dependencies
├── backend/
│   ├── app/
│   │   ├── models/           # Database models
│   │   ├── services/         # Email, QR code generation
│   │   └── core/             # Config, database, security
│   └── requirements.txt      # Backend-specific dependencies
├── requirements.txt          # Combined dependencies (for Streamlit Cloud)
├── runtime.txt              # Python version
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── .gitignore               # Files to ignore in Git
```

---

## Environment Variables

### Required Secrets (in Streamlit Cloud):
| Variable | Description | Example |
|----------|-------------|---------|
| `GMAIL_ADDRESS` | Gmail email for sending passes | Swavlamban2025@gmail.com |
| `GMAIL_APP_PASSWORD` | 16-char app password | pwiwmzgshilvmeon |
| `USE_GMAIL_SMTP` | Enable Gmail SMTP | true |
| `JWT_SECRET_KEY` | Secret for JWT tokens | random-secret-key |

### Optional Secrets:
| Variable | Description |
|----------|-------------|
| `MAILBLUSTER_API_KEY` | MailBluster API key (if using) |
| `DEBUG` | Enable debug mode (false in production) |

---

## Python Version

**Streamlit Cloud uses Python 3.11.6** (specified in `runtime.txt`)

**Why Python 3.11?**
- ✅ Stable and well-tested
- ✅ Compatible with all dependencies
- ✅ Officially supported by Streamlit Cloud
- ✅ Better performance than 3.9/3.10

**Note**: Python 3.14 doesn't exist yet. Latest stable is 3.12, but we use 3.11.6 for maximum compatibility.

---

## ⚠️ CRITICAL: Database Configuration

### Development (Local):
- **Type**: SQLite
- **File**: `swavlamban2025.db`
- **Location**: Root directory
- **Persistence**: ✅ Data persists locally

### Production (Streamlit Cloud):

**⚠️ WARNING: DO NOT USE SQLITE ON STREAMLIT CLOUD!**

Streamlit Cloud uses **ephemeral file system**:
- ❌ SQLite database is **DELETED on every restart**
- ❌ All data is **LOST** when you update/redeploy
- ❌ **NOT suitable for production**

### ✅ Required: PostgreSQL with External Hosting

**You MUST use external PostgreSQL for production.**

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for complete setup guide.

### ✅ Your Supabase Configuration (ALREADY SET UP)

You have already created a Supabase database. Use these credentials in Streamlit Cloud secrets:

```toml
DB_HOST = "db.scvzcvpyvmwzigusdjsl.supabase.co"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "your-supabase-database-password-here"
```

**⚠️ IMPORTANT**: You must add your Supabase database password (the one you created when setting up the Supabase project) to make this work.

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed Supabase setup instructions.

---

## Email Service Configuration

### Gmail SMTP (Recommended - FREE):
- **Daily Limit**: 500 emails
- **Cost**: $0
- **Reliability**: High
- **Setup**: App Password from Google

### MailBluster (Alternative):
- **Requires**: Paid SMTP provider
- **Better for**: Large scale (10,000+ emails)

---

## Security Checklist

Before going live:

- [ ] Changed default admin password
- [ ] Set strong JWT_SECRET_KEY in secrets
- [ ] Enabled HTTPS (automatic on Streamlit Cloud)
- [ ] Verified .env files are NOT committed to Git
- [ ] Tested email sending works
- [ ] Configured proper user permissions
- [ ] Set repository to Private on GitHub
- [ ] Disabled DEBUG mode in production

---

## Monitoring & Maintenance

### Check Logs:
- Streamlit Cloud dashboard → Your app → Logs
- Monitor for errors during email sending
- Watch for database connection issues

### Update Dependencies:
```bash
# Check for outdated packages
pip list --outdated

# Update requirements.txt as needed
pip freeze > requirements.txt
```

### Backup Database:
For SQLite on Streamlit Cloud, database is ephemeral. For production:
- Use PostgreSQL with automated backups
- Or implement manual CSV export feature (already included in Admin Panel)

---

## Troubleshooting

### Common Issues:

#### 1. "ModuleNotFoundError"
- **Cause**: Missing dependency in requirements.txt
- **Fix**: Add the package to root requirements.txt and redeploy

#### 2. Email Not Sending
- **Cause**: Invalid Gmail App Password
- **Fix**: Regenerate app password and update secrets

#### 3. Database Errors
- **Cause**: Database file doesn't exist
- **Fix**: App should auto-create on first run

#### 4. "Port already in use"
- **Cause**: Multiple Streamlit instances
- **Fix**: Streamlit Cloud handles this automatically

---

## Support

### Documentation:
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Gmail SMTP: See GMAIL_SMTP_SETUP.md
- MailBluster: See MAILBLUSTER_SETUP.md

### Contact:
- **Support**: niio-tdac@navy.gov.in
- **GitHub Issues**: Create issue in repository

---

## Quick Deployment Checklist

- [ ] Code pushed to GitHub (private repository)
- [ ] Streamlit Cloud account created
- [ ] App deployed (frontend/app.py as entry point)
- [ ] Secrets configured in Streamlit Cloud
- [ ] Database initialized
- [ ] Admin password changed
- [ ] Email sending tested
- [ ] Organization users created
- [ ] Pass permissions configured
- [ ] Security checklist completed
- [ ] Ready for production use!

---

## App URL

After deployment, your app will be accessible at:
```
https://YOUR_APP_NAME.streamlit.app
```

Example: `https://swavlamban2025.streamlit.app`

---

**Deployment Status**: ✅ Ready
**Python Version**: 3.11.6
**Cost**: $0 (Streamlit Cloud Free Tier)
**Email Limit**: 500/day (Gmail SMTP)

---

Last Updated: 2025-10-21
Version: 2.0
