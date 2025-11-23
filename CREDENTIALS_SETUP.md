# Swavlamban 2025 - Credentials & Environment Setup

## 🔑 Required Credentials (From 2024 System)

The 2024 system used **Streamlit Secrets** for credential management. Here are all the required credentials:

---

## 📧 Mailjet Email Service

### Required Secrets:
```
MAILJET_API_KEY=your_mailjet_api_key
MAILJET_API_SECRET=your_mailjet_api_secret
EMAIL_SENDER=noreply@yourdomain.com
```

### Purpose:
- Send registration confirmation emails
- Deliver passes with QR codes
- Send bulk announcements
- Attach event documents (venue maps, guidelines)

### Where to Get:
1. Log in to Mailjet account
2. Go to **Account Settings** → **API Keys**
3. Copy API Key and API Secret
4. Configure sender email (must be verified in Mailjet)

### Mailjet Limits:
- Free tier: 6,000 emails/month, 200 emails/day
- Paid tier recommended for 1,500+ attendees

---

## 🐙 GitHub Personal Access Token (PAT)

### Required Secret:
```
GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Purpose:
- Push database updates to GitHub
- Version control for data backup
- Sync changes to repository

### Where to Get:
1. GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token (classic)**
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (if using GitHub Actions)
4. Generate token and copy immediately (shown only once)

### GitHub Repository:
- **2024 Repo**: https://github.com/0xHKG/swavlamban24
- **2025 Repo**: TBD (create new or reuse?)

---

## 🗄️ Database Credentials (If Using PostgreSQL for 2025)

### Required Secrets (for PostgreSQL):
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=swavlamban2025
DB_USER=swavlamban_user
DB_PASSWORD=secure_password_here
DB_SSLMODE=require
```

### Note:
- 2024 used SQLite (no credentials needed)
- 2025 will use PostgreSQL (needs credentials)
- Consider using managed database (AWS RDS, DigitalOcean Managed DB)

---

## 🔒 Redis Cache Credentials (For 2025)

### Required Secrets:
```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis_password_here
REDIS_DB=0
```

### Purpose:
- Session management
- Rate limiting
- Caching user data

---

## 📁 Streamlit Secrets Configuration

### For Streamlit Cloud Deployment:

1. Go to your Streamlit Cloud app
2. Click **Settings** → **Secrets**
3. Add secrets in TOML format:

```toml
# .streamlit/secrets.toml

# Mailjet Email Service
MAILJET_API_KEY = "your_api_key_here"
MAILJET_API_SECRET = "your_api_secret_here"
EMAIL_SENDER = "noreply@swavlamban2025.in"

# GitHub (for backup/sync)
GITHUB_PAT = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# PostgreSQL Database (2025)
DB_HOST = "your-db-host.com"
DB_PORT = "5432"
DB_NAME = "swavlamban2025"
DB_USER = "swavlamban_user"
DB_PASSWORD = "secure_password"
DB_SSLMODE = "require"

# Redis Cache (2025)
REDIS_HOST = "your-redis-host.com"
REDIS_PORT = "6379"
REDIS_PASSWORD = "redis_password"
REDIS_DB = "0"

# JWT Secret (2025 - for authentication)
JWT_SECRET_KEY = "generate-a-long-random-string-here"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = "15"

# Admin Credentials (2025)
ADMIN_USERNAME = "tdac"
ADMIN_EMAIL = "admin@swavlamban2025.in"
```

---

## 🔐 Local Development Setup

### Option 1: Using .env File (NOT committed to git)

Create `.env` file in project root:

```bash
# .env (DO NOT COMMIT TO GIT)

# Mailjet
MAILJET_API_KEY=your_api_key
MAILJET_API_SECRET=your_api_secret
EMAIL_SENDER=noreply@localhost

# GitHub
GITHUB_PAT=ghp_xxxxxxxxxxxxx

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=swavlamban2025
DB_USER=postgres
DB_PASSWORD=postgres
DB_SSLMODE=prefer

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# JWT
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
```

### Load .env in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()

MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
```

### Option 2: Using Streamlit Secrets (Local)

Create `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml (DO NOT COMMIT TO GIT)

MAILJET_API_KEY = "your_api_key"
MAILJET_API_SECRET = "your_api_secret"
EMAIL_SENDER = "noreply@localhost"
GITHUB_PAT = "ghp_xxxxxxxxxxxxx"

# ... rest of secrets
```

Access in code:
```python
import streamlit as st

api_key = st.secrets["MAILJET_API_KEY"]
```

---

## 🚨 Security Best Practices

### Do's ✅
- ✅ Use environment variables for all secrets
- ✅ Use different credentials for dev/staging/production
- ✅ Rotate credentials regularly (every 90 days)
- ✅ Use strong, random passwords (minimum 32 characters)
- ✅ Enable 2FA on all service accounts
- ✅ Use managed services (reduces credential exposure)
- ✅ Add `.env` and `secrets.toml` to `.gitignore`
- ✅ Use secret management tools (AWS Secrets Manager, HashiCorp Vault)

### Don'ts ❌
- ❌ Never commit credentials to git
- ❌ Never hardcode secrets in source code
- ❌ Never share credentials via email/chat
- ❌ Never use production credentials for development
- ❌ Never reuse passwords across services
- ❌ Never log secrets (even in debug mode)

---

## 🔄 Migrating from 2024 to 2025

### Credentials to Reuse:
1. **Mailjet API Keys** - ✅ Same account, same keys
2. **Email Sender** - ✅ Same or update domain
3. **GitHub PAT** - ✅ Can reuse or generate new

### New Credentials Needed:
1. **PostgreSQL** - ⚠️ New database, new credentials
2. **Redis** - ⚠️ New cache server, new credentials
3. **JWT Secret** - ⚠️ Generate new random secret

---

## 📝 Credential Generation Guide

### Generate JWT Secret Key:
```python
import secrets
jwt_secret = secrets.token_urlsafe(32)
print(jwt_secret)
# Output: "xK8j3mP9qL2vN7wR4tY6uI1oP0aS5dF8gH3jK6lZ9xC2vB5nM8"
```

### Generate Strong Password:
```python
import secrets
import string

alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for i in range(32))
print(password)
```

### Generate API Key (for custom services):
```python
import uuid
api_key = str(uuid.uuid4())
print(api_key)
# Output: "550e8400-e29b-41d4-a716-446655440000"
```

---

## 🧪 Testing Credentials

### Test Mailjet Connection:
```python
from mailjet_rest import Client
import os

api_key = os.getenv("MAILJET_API_KEY")
api_secret = os.getenv("MAILJET_API_SECRET")

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# Test connection
try:
    result = mailjet.send.create(data={
        'Messages': [{
            "From": {"Email": "noreply@yourdomain.com", "Name": "Test"},
            "To": [{"Email": "your-email@example.com"}],
            "Subject": "Test Email",
            "TextPart": "Testing Mailjet connection"
        }]
    })
    print(f"Success! Status: {result.status_code}")
except Exception as e:
    print(f"Error: {e}")
```

### Test PostgreSQL Connection:
```python
import psycopg2
import os

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    print("PostgreSQL connection successful!")
    conn.close()
except Exception as e:
    print(f"PostgreSQL connection failed: {e}")
```

### Test Redis Connection:
```python
import redis
import os

try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        password=os.getenv("REDIS_PASSWORD"),
        db=int(os.getenv("REDIS_DB"))
    )
    r.ping()
    print("Redis connection successful!")
except Exception as e:
    print(f"Redis connection failed: {e}")
```

---

## 📦 Required Python Packages

Add to `requirements.txt`:

```txt
# Email
mailjet-rest==1.3.4

# Database
psycopg2-binary==2.9.9
SQLAlchemy==2.0.23

# Cache
redis==5.0.1

# Security
python-dotenv==1.0.0
bcrypt==4.1.1
PyJWT==2.8.0
cryptography==41.0.7

# Others (from 2024)
streamlit==1.25.0
gitpython==3.1.32
qrcode==7.3
Pillow==9.2.0
pandas==1.4.3
```

---

## ❓ Questions to Resolve

### 1. Mailjet Account
- ❓ Do you still have access to the 2024 Mailjet account?
- ❓ What are the API keys? (I can help you retrieve if you provide login)
- ❓ What email sender address was used? (noreply@...?)

### 2. GitHub
- ❓ Should we reuse the `0xHKG/swavlamban24` repo or create `swavlamban25`?
- ❓ Do you have the GitHub PAT from 2024?
- ❓ If not, can you generate a new one?

### 3. Database (New for 2025)
- ❓ Preferred database provider? (AWS RDS, DigitalOcean, Heroku, etc.)
- ❓ Should I help set up PostgreSQL locally for development?

### 4. Deployment
- ❓ Will you deploy on Streamlit Cloud (like 2024) or custom server?
- ❓ Do you have Streamlit Cloud account access from 2024?

---

## 📋 Checklist for Getting Started

### Immediate Actions:
- [ ] Retrieve Mailjet API keys from 2024 account
- [ ] Retrieve/generate GitHub PAT
- [ ] Confirm email sender address
- [ ] Decide on GitHub repository (reuse or new)

### For Development Setup:
- [ ] Install PostgreSQL locally
- [ ] Install Redis locally
- [ ] Create `.env` file with credentials
- [ ] Test all connections
- [ ] Generate JWT secret key

### For Production Deployment:
- [ ] Setup managed PostgreSQL (AWS/DigitalOcean)
- [ ] Setup managed Redis
- [ ] Configure Streamlit Cloud secrets
- [ ] Test production credentials
- [ ] Setup monitoring & alerts

---

## 🔗 Useful Links

- **Mailjet Dashboard**: https://app.mailjet.com/
- **GitHub PAT Settings**: https://github.com/settings/tokens
- **Streamlit Cloud**: https://share.streamlit.io/
- **AWS RDS**: https://aws.amazon.com/rds/
- **DigitalOcean Managed DB**: https://www.digitalocean.com/products/managed-databases

---

## 💬 Need Help?

If you need help retrieving or setting up any credentials:
1. Provide access to accounts (Mailjet, GitHub, etc.)
2. I can help generate secure secrets
3. I can set up local development environment
4. I can configure production deployment

---

**Status**: ⏳ Awaiting credential information
**Priority**: High (needed before development)
**Next Action**: Retrieve Mailjet & GitHub credentials from 2024 system
