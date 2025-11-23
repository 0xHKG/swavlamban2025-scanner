# NIC SMTP Setup Guide for Swavlamban 2025

## 🎯 Overview

This guide explains how to configure **NIC SMTP** (smtp.mgovcloud.in) to send emails from your official Government/Navy email address (`niio-tdac@navy.gov.in`).

**Official Documentation**: https://www.mgovcloud.in/mail/help/nic-smtp.html

**Benefits:**
- ✅ **Official Email Address**: Recipients see `niio-tdac@navy.gov.in` (more professional than Gmail)
- ✅ **Higher Deliverability**: Government domain emails have better trust/reputation
- ✅ **No Daily Limits**: Unlike Gmail's 500 emails/day limit
- ✅ **100% FREE**: No cost for government users
- ✅ **Secure**: TLS/SSL encryption supported

---

## 📋 Prerequisites

You need:
1. Access to your NIC email account: `niio-tdac@navy.gov.in`
2. Your NIC email password
3. *(Optional)* Application-specific password if 2FA is enabled

---

## 🔧 Configuration Steps

### Step 1: Update `.env` File

Edit the `.env` file in the `backend` directory:

```bash
cd swavlamban2025/backend
nano .env  # or use your preferred text editor
```

### Step 2: Add NIC SMTP Settings

Add these lines to your `.env` file:

```env
# NIC SMTP Configuration (RECOMMENDED)
USE_NIC_SMTP=true
NIC_EMAIL_ADDRESS=niio-tdac@navy.gov.in
NIC_EMAIL_PASSWORD=your_actual_password_here

# Disable other email providers
USE_GMAIL_SMTP=false
```

**Important:** Replace `your_actual_password_here` with your actual NIC email password.

### Step 3: If Using Two-Factor Authentication (2FA)

If your NIC email has 2FA enabled:

1. Login to NIC Mail: https://mail.gov.in
2. Go to **Settings** → **Security**
3. Generate an **Application-Specific Password**
4. Use this app-specific password in `.env` instead of your regular password

---

## 📧 NIC SMTP Server Details

### ⚠️ CRITICAL UPDATE (2025-10-23): USE SSL (PORT 465) ONLY!

**IMPORTANT:** After testing on 2025-10-23, **SSL (port 465) is the ONLY working method** for App-Specific Passwords.

| Setting | Value | Status |
|---------|-------|--------|
| **SMTP Server** | smtp.mgovcloud.in | ✅ Working |
| **Port (SSL)** | **465 with SSL** | ✅ **RECOMMENDED - WORKS** |
| **Port (TLS)** | ~~587 with TLS~~ | ❌ **Authentication Failed** |
| **Encryption** | SSL (SMTP_SSL) | ✅ Required |
| **Authentication** | Required - YES | ✅ Working |
| **Username Format** | Full email address: `username@nic.in` or `username@navy.gov.in` | ✅ Correct |
| **Password** | Application-Specific Password (MANDATORY) | ✅ Working |

### Working Configuration (Tested 2025-10-23):
```
Server: smtp.mgovcloud.in
Port: 465
Protocol: SSL (SMTP_SSL - NOT STARTTLS)
Email: niio-tdac@navy.gov.in
Password: cXpg0GHMzqqZ (App-Specific Password)
Result: ✅ Authentication Successful
```

### Official Configuration (from mgovcloud.in)

According to official documentation, both ports are supported:
- Port 465 with SSL ✅ (Currently working)
- Port 587 with TLS ❌ (Authentication failing as of Oct 2025)

**Note:** TLS (port 587) was working on Oct 22, 2025, but stopped working on Oct 23, 2025. NIC Mail server likely changed TLS/STARTTLS requirements. **Use SSL (port 465) only.**

**IMPORTANT NOTES:**
1. **Username must be complete email address** (e.g., `niio-tdac@navy.gov.in`, not just `niio-tdac`)
2. **Two-Factor Authentication**: If 2FA is enabled, you MUST use an Application-Specific Password
3. **Email Address Match**: The From address must exactly match your authenticated email address
4. **Relaying Error**: If you see "Relaying Disallowed", your From address doesn't match your login credentials

### Getting Application-Specific Password:
1. Login to NIC Mail: https://mail.gov.in
2. Go to **Settings** → **Security**
3. Generate an **Application-Specific Password**
4. Use this password (without spaces) in your configuration

---

## 🧪 Testing the Configuration

### Option 1: Run Test Script

Create a test script to verify SMTP connection:

```python
# test_nic_smtp.py
import sys
sys.path.append('backend')

from app.services.nic_smtp_service import NICSmtpService

# Test connection
smtp_service = NICSmtpService()
if smtp_service.test_connection():
    print("✅ NIC SMTP is configured correctly!")
else:
    print("❌ NIC SMTP configuration failed. Check your credentials.")
```

Run it:
```bash
cd swavlamban2025
python3 test_nic_smtp.py
```

### Option 2: Use the Application

1. Start the application:
   ```bash
   cd swavlamban2025
   streamlit run frontend/app.py
   ```

2. Login with your admin credentials
3. Go to **Generate Passes** tab
4. Create a test entry
5. Try sending an email
6. Check the console output for:
   ```
   📧 Sending email via NIC SMTP (Navy Email)...
   ✅ Email sent successfully to recipient@example.com via NIC SMTP
   ```

---

## 🔍 Troubleshooting

### Issue 1: Authentication Failed

**Error**: `Authentication failed` or `Login failed`

**Solutions:**
- ✅ Verify your NIC email address is correct: `niio-tdac@navy.gov.in`
- ✅ Check your password (no typos, correct case)
- ✅ If using 2FA, generate and use an application-specific password
- ✅ Try logging into https://mail.gov.in with the same credentials

### Issue 2: Connection Timeout

**Error**: `Connection timeout` or `Cannot connect to SMTP server`

**Solutions:**
- ✅ Check firewall settings (allow outbound connections to port 587)
- ✅ Verify internet connectivity
- ✅ Try alternative port 465 (edit `nic_smtp_service.py` line 23)

### Issue 3: "Relaying Disallowed"

**Error**: `Relaying disallowed` or `Relay access denied`

**Solutions:**
- ✅ Ensure email address matches authenticated account
- ✅ Use complete email address: `niio-tdac@navy.gov.in` (not just username)
- ✅ Verify authentication credentials are correct

### Issue 4: Email Not Received

**Error**: Email sends successfully but recipient doesn't receive it

**Solutions:**
- ✅ Check recipient's spam/junk folder
- ✅ Verify recipient email address is correct
- ✅ Check email server logs for delivery status
- ✅ Try sending to a different email address (Gmail, Outlook) to test

---

## 📱 Email Provider Priority

The system checks email providers in this order:

1. **NIC SMTP** (if `USE_NIC_SMTP=true` and credentials configured)
2. **Gmail SMTP** (if `USE_GMAIL_SMTP=true` and credentials configured)
3. **MailBluster** (if API key configured)
4. **Mailjet** (legacy fallback)

To use NIC SMTP as primary:
```env
USE_NIC_SMTP=true
USE_GMAIL_SMTP=false
```

To use Gmail as backup:
```env
USE_NIC_SMTP=true
USE_GMAIL_SMTP=true  # Falls back to Gmail if NIC fails
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` to Git**
   - `.env` is in `.gitignore` by default
   - Never share your password publicly

2. **Use Application-Specific Passwords**
   - If your account has 2FA, generate app passwords
   - Safer than using your main password

3. **Rotate Passwords Regularly**
   - Change passwords periodically
   - Update `.env` when you change password

4. **Restrict File Permissions**
   ```bash
   chmod 600 backend/.env
   ```

---

## 🚀 Deployment to Streamlit Cloud

When deploying to Streamlit Cloud, add these secrets:

1. Go to Streamlit Cloud → Your App → Settings → Secrets
2. Add:
   ```toml
   # NIC SMTP Configuration
   USE_NIC_SMTP = true
   NIC_EMAIL_ADDRESS = "niio-tdac@navy.gov.in"
   NIC_EMAIL_PASSWORD = "your_actual_password_here"
   USE_GMAIL_SMTP = false
   ```

---

## 🔧 Troubleshooting Common Issues

### 1. Authentication Failed (Error 535)

**Symptom**: `(535, b'Authentication Failed')`

**Possible Causes & Solutions**:

#### a) Two-Factor Authentication Enabled
- **Problem**: Using regular password when 2FA is enabled
- **Solution**: Generate and use Application-Specific Password
  1. Login to https://mail.gov.in
  2. Go to **Settings** → **Security**
  3. Generate **Application-Specific Password**
  4. Use this password (format: `yLjbhK09Ad29` - no spaces)

#### b) Incorrect Username Format
- **Problem**: Using username only instead of full email
- **Wrong**: `niio-tdac`
- **Correct**: `niio-tdac@navy.gov.in`

#### c) Password Contains Special Characters
- **Problem**: Special characters in password not properly escaped
- **Solution**: Ensure password is copied exactly as generated
- **Check**: No extra spaces, quotes, or line breaks

#### d) Credentials Not Loading from Secrets
- **Problem**: Streamlit Cloud not reading secrets correctly
- **Solution**: Check debug logs for:
  ```
  🔑 Loaded NIC SMTP from secrets: niio-tdac@navy.gov.in
  ✅ Successfully loaded configuration from Streamlit secrets
  ```
- If not shown, verify Streamlit Cloud secrets configuration

### 2. Unable to Connect to SMTP Server

**Symptom**: `Name or service not known` or `Connection refused`

**Solutions**:
- Verify server name is exactly: `smtp.mgovcloud.in` (not `smtp.mygovcloud.in`)
- Check port: 587 (TLS) or 465 (SSL)
- Verify firewall isn't blocking ports 587/465
- Test DNS resolution:
  ```bash
  nslookup smtp.mgovcloud.in
  # Should return: 169.148.142.84
  ```

### 3. Relaying Disallowed Error

**Symptom**: Email rejected with "Relaying Disallowed"

**Cause**: From email address doesn't match authenticated credentials

**Solutions**:
- Ensure `NIC_EMAIL_ADDRESS` matches the email you're sending FROM
- Check code uses `settings.NIC_EMAIL_ADDRESS` as sender
- Verify no hardcoded different email address in code

### 4. Duplicate Sent Emails

**Symptom**: Two copies of sent emails in Sent folder

**Solution**:
1. Login to https://mail.gov.in/
2. Go to **Settings** → **Mail Accounts**
3. Click your email address
4. Under **SMTP** section, uncheck **'Save copy of sent emails'**

### 5. Connection Timeout

**Symptom**: Timeout when connecting to SMTP server

**Solutions**:
- Check your network/internet connection
- Verify firewall rules allow outbound connections to port 587/465
- Try alternative port (587 vs 465)
- Contact NIC Support with traceroute:
  ```bash
  traceroute smtp.mgovcloud.in
  ```

### 6. Email Not Received (Sent Successfully)

**Symptom**: Email shows as sent but recipient doesn't receive it

**Solutions**:
- Check recipient's spam/junk folder
- Verify recipient email address is correct
- Check NIC Mail sent folder to confirm email was sent
- Wait a few minutes (delivery delays can occur)
- Contact NIC Support with message details

---

## 📞 Support

### NIC Email Support
- **Email**: helpdesk-email@gov.in
- **Phone**: 1800-571-9646 (24/7 toll-free)
- **Web**: https://www.mgovcloud.in/mail/
- **Help Documentation**: https://www.mgovcloud.in/mail/help/nic-smtp.html

### Application Support
- Check application logs in console
- Review `CLAUDE.md` for troubleshooting
- Contact TDAC team for deployment issues

---

## ✅ Configuration Checklist

- [ ] NIC email credentials verified (can login to https://mail.gov.in)
- [ ] `.env` file updated with NIC SMTP settings
- [ ] `USE_NIC_SMTP=true` set
- [ ] `USE_GMAIL_SMTP=false` (or as backup)
- [ ] Application-specific password generated (if using 2FA)
- [ ] Test connection successful
- [ ] Test email sent and received
- [ ] Production deployment configured (Streamlit secrets)

---

## 📊 Comparison: NIC SMTP vs Gmail SMTP

| Feature | NIC SMTP | Gmail SMTP |
|---------|----------|------------|
| **Email Address** | niio-tdac@navy.gov.in | Swavlamban2025@gmail.com |
| **Professional** | ✅ Official govt email | ⚠️ Personal email |
| **Daily Limit** | Unlimited (likely) | 500 emails/day |
| **Deliverability** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good |
| **Cost** | FREE | FREE |
| **Setup Difficulty** | Easy | Easy |
| **Reliability** | High | High |
| **Best For** | Production use | Testing/Development |

**Recommendation**: Use **NIC SMTP** for production deployment to maintain professional communication from an official Navy email address.

---

**Last Updated**: 2025-10-22
**Version**: 1.0
**Status**: ✅ Production Ready
