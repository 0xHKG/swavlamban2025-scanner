# Gmail SMTP Integration - 100% FREE Email Sending

## Why Gmail SMTP?

**Completely FREE** - No third-party service needed!
- **No API costs** - Uses your Gmail account
- **500 emails/day** - Free Gmail limit
- **No credit card required**
- **No SMTP provider fees** (unlike MailBluster's providers)
- **Built into Python** - No external dependencies

---

## Step-by-Step Setup (5 Minutes)

### Step 1: Enable 2-Factor Authentication on Gmail

1. **Go to Google Account Security**: https://myaccount.google.com/security
2. **Find "2-Step Verification"** section
3. **Click "Get Started"** (if not already enabled)
4. **Follow the wizard** to enable 2FA using your phone

> **Note**: App Passwords require 2FA to be enabled first!

---

### Step 2: Generate App Password

1. **Go to App Passwords**: https://myaccount.google.com/apppasswords
   - Or navigate: Google Account → Security → 2-Step Verification → App passwords

2. **Select app**: Choose **"Mail"**

3. **Select device**: Choose **"Other (Custom name)"**
   - Enter: `Swavlamban 2025 System`

4. **Click "Generate"**

5. **Copy the 16-character password**
   - Example: `abcd efgh ijkl mnop`
   - Remove spaces: `abcdefghijklmnop`

6. **Keep this password safe!** You'll need it in the next step.

---

### Step 3: Configure Your System

1. **Open the `.env` file**:
   ```bash
   cd /home/santosh/Desktop/Swavlamban\ 2025/swavlamban2025/backend
   nano .env
   ```

2. **Update Gmail settings** (around line 19):
   ```bash
   # Replace with YOUR actual Gmail credentials
   GMAIL_ADDRESS=your-actual-email@gmail.com
   GMAIL_APP_PASSWORD=abcdefghijklmnop  # 16-char password from Step 2
   USE_GMAIL_SMTP=true
   ```

3. **Save the file** (Ctrl+O, Enter, Ctrl+X)

---

### Step 4: Restart Streamlit

Since the frontend is already running, you need to restart it to load the new configuration:

1. **Stop Streamlit** (Ctrl+C in the terminal running it)

2. **Restart Streamlit**:
   ```bash
   cd /home/santosh/Desktop/Swavlamban\ 2025/swavlamban2025/frontend
   streamlit run app.py
   ```

3. **Refresh browser**: http://localhost:8501

---

### Step 5: Test Email Sending

#### Quick Test:

1. **Login as admin** (username: `admin`, password: `admin123`)
2. **Go to Admin Panel**
3. **Click "📧 Send Bulk Email"** under Quick Actions
4. **Configure test email**:
   - **Recipients**: Select "All Attendees" or just one person
   - **Subject**: `Test Email - Swavlamban 2025`
   - **Message**: `This is a test email to verify Gmail SMTP integration.`
5. **Click "📤 Send Bulk Email"**
6. **Check your inbox!**

---

## How It Works

### Gmail SMTP Server Details:
- **Server**: `smtp.gmail.com`
- **Port**: `587` (TLS encryption)
- **Authentication**: Your Gmail address + App Password
- **Protocol**: STARTTLS (secure connection)

### What Happens When You Send Email:
1. System creates HTML email with attachments (if any)
2. Connects to Gmail's SMTP server using TLS
3. Authenticates with your Gmail credentials
4. Sends email through Gmail's infrastructure
5. Gmail delivers to recipient's inbox

### Email Format:
- **From**: `Swavlamban 2025 <your-gmail@gmail.com>`
- **HTML Content**: Professional templates with Indian Navy branding
- **Attachments**: QR code passes as PNG files
- **Delivery**: Through Gmail's reliable infrastructure

---

## Features Available

All email features work with Gmail SMTP:

### ✅ Individual Pass Emails
- Generate passes for attendee
- Automatically send email with QR codes attached
- Professional HTML templates for each pass type

### ✅ Bulk Emails
- Send to all attendees
- Filter by pass type (Exhibition, Panel, Plenary)
- Filter by organization
- Optional: Include QR passes as attachments
- Progress tracking with success/failure counts

### ✅ Email Templates
Pre-built templates for all 5 pass types:
1. **Exhibition Day 1** - Navy blue theme
2. **Exhibition Day 2** - Gray theme
3. **Panel Discussion I** - Green theme
4. **Panel Discussion II** - Blue theme
5. **Plenary Session** - Brown theme

All include:
- Event details (date, time, venue)
- Indian Navy branding
- Support contact info
- QR code pass attachments

---

## Limits & Best Practices

### Gmail Sending Limits:
- **500 emails per day** (rolling 24-hour period)
- **500 recipients per email** (for bulk sends)
- **25 MB per email** (including attachments)

### Best Practices:
1. **Don't exceed 500/day** - Spread bulk sends across multiple days if needed
2. **Monitor bounces** - Check Gmail Sent folder for delivery failures
3. **Use descriptive subjects** - Helps avoid spam filters
4. **Test first** - Send to yourself before bulk sending
5. **Keep attachments small** - QR code passes are ~50KB each (well within limit)

### Rate Limiting:
The system sends emails **sequentially** (one at a time) to avoid:
- Gmail rate limits
- Connection timeouts
- IP blocking

---

## Troubleshooting

### ❌ Error: "Username and Password not accepted"

**Causes**:
1. App Password incorrect
2. 2FA not enabled
3. Copy-pasted password has spaces

**Solutions**:
1. **Regenerate App Password** at https://myaccount.google.com/apppasswords
2. **Ensure 2FA is enabled** on your Google account
3. **Remove spaces** from app password in `.env` file
4. **Check Gmail address** is spelled correctly

---

### ❌ Error: "SMTP connection failed"

**Causes**:
1. Firewall blocking port 587
2. No internet connection
3. Gmail SMTP server temporarily down

**Solutions**:
1. **Check internet connection**
2. **Test Gmail SMTP manually**:
   ```python
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email@gmail.com', 'your-app-password')
   print("✅ Connection successful!")
   server.quit()
   ```
3. **Check firewall settings** - Allow outbound port 587

---

### ❌ Error: "Email sent but not received"

**Causes**:
1. Email in spam folder
2. Invalid recipient email
3. Recipient server rejected email

**Solutions**:
1. **Check spam/junk folder**
2. **Check Gmail Sent folder** to verify it was sent
3. **Test with your own email first**
4. **Verify recipient email is valid**

---

### ❌ Error: "Exceeded daily sending limit"

**Cause**: Sent more than 500 emails in 24 hours

**Solutions**:
1. **Wait 24 hours** for limit to reset
2. **Use multiple Gmail accounts** and distribute sends
3. **Spread bulk sends across multiple days**
4. **Check Gmail dashboard** for exact limit reset time

---

## Comparison: Gmail SMTP vs MailBluster

| Feature | Gmail SMTP | MailBluster |
|---------|-----------|-------------|
| **Cost** | ✅ **100% FREE** | ❌ Requires paid SMTP provider |
| **Setup Time** | 5 minutes | 15-30 minutes |
| **Daily Limit** | 500 emails | Depends on SMTP provider |
| **Reliability** | Google's infrastructure | Depends on SMTP provider |
| **Attachments** | ✅ Yes (25MB total) | ✅ Yes |
| **HTML Emails** | ✅ Yes | ✅ Yes |
| **Analytics** | Basic (Gmail Sent folder) | Advanced (MailBluster dashboard) |
| **Bounce Handling** | Manual (check Sent folder) | Automatic |
| **Unsubscribe** | Manual | Automatic |
| **Campaigns** | No (bulk send only) | Yes |

**Recommendation**:
- **For this event (500-1000 attendees)**: Gmail SMTP is perfect and FREE
- **For large scale (10,000+ emails)**: Consider MailBluster with paid SMTP

---

## Advanced: Switching Between Services

The system supports both Gmail SMTP and MailBluster. You can switch by changing the `.env` file:

### Use Gmail SMTP (Recommended - FREE):
```bash
USE_GMAIL_SMTP=true
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

### Use MailBluster (If you have paid SMTP):
```bash
USE_GMAIL_SMTP=false
MAILBLUSTER_API_KEY=your-api-key
```

The frontend will automatically use the configured service!

---

## Security Best Practices

### ✅ DO:
1. **Keep `.env` file secret** - Already in `.gitignore`
2. **Use App Passwords** - Never use your actual Gmail password
3. **Revoke unused App Passwords** - Clean up old passwords in Google Account
4. **Use separate Gmail account** - Consider creating `swavlamban2025@gmail.com`
5. **Monitor sent folder** - Watch for bounces or issues

### ❌ DON'T:
1. **Never commit `.env` to Git** - Contains credentials
2. **Never share App Password** - Treat like a password
3. **Never use personal Gmail** - Use dedicated account for event
4. **Never exceed limits** - Respect Gmail's 500/day limit
5. **Never send spam** - Only send to registered attendees

---

## Testing Checklist

Before sending to attendees, test:

- [ ] Send email to yourself
- [ ] Check HTML formatting looks correct
- [ ] Verify QR code attachments are included
- [ ] Test with different email providers (Gmail, Outlook, Yahoo)
- [ ] Check spam score (use https://www.mail-tester.com)
- [ ] Verify "From" name shows "Swavlamban 2025"
- [ ] Test links in email work correctly
- [ ] Send to colleague for review
- [ ] Confirm subject line is professional
- [ ] Ready to send to attendees!

---

## Support

### Gmail SMTP Issues:
- **Gmail Help**: https://support.google.com/mail
- **App Passwords Help**: https://support.google.com/accounts/answer/185833
- **SMTP Documentation**: https://support.google.com/a/answer/176600

### Application Issues:
- Check terminal logs for error messages
- Verify `.env` file is loaded correctly
- Test SMTP connection manually (see Troubleshooting section)
- Check Gmail Sent folder for delivery status

---

## Quick Reference

### Gmail Account Settings:
```
SMTP Server: smtp.gmail.com
Port: 587
Encryption: STARTTLS
Authentication: Yes
Username: your-email@gmail.com
Password: 16-char App Password
```

### Files Modified:
1. `backend/.env` - Added Gmail credentials
2. `backend/app/services/gmail_smtp_service.py` - Gmail SMTP service (already created)
3. `backend/app/core/config.py` - Gmail settings (already added)

### Next Steps After Setup:
1. ✅ Configure Gmail credentials in `.env`
2. ✅ Restart Streamlit
3. ✅ Send test email to yourself
4. ✅ Review email in inbox
5. ✅ Send to attendees!

---

## Summary

**Gmail SMTP is the recommended solution because:**
- ✅ **100% FREE** - No costs at all
- ✅ **No setup complexity** - Just Gmail credentials
- ✅ **Reliable** - Google's infrastructure
- ✅ **500 emails/day** - Enough for this event
- ✅ **Professional** - Emails from Gmail are trusted
- ✅ **Secure** - TLS encryption + App Passwords

**Total setup time: 5 minutes**

**Status**: ✅ Ready to use!

---

Last Updated: 2025-10-21
Version: 1.0
Support: niio-tdac@navy.gov.in
