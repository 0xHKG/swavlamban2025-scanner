# MailBluster Integration Setup Guide

## 📧 Complete Guide to Send Emails via MailBluster

This guide will help you configure MailBluster to send emails from the Swavlamban 2025 registration system.

---

## Step 1: Get Your MailBluster API Key

1. **Login to MailBluster**: https://app.mailbluster.com
2. **Go to Brand Settings**:
   - Click on your brand name
   - Navigate to **Settings**
3. **Access API Keys Tab**:
   - Click on **API keys** under Settings
4. **Create New API Key**:
   - Click the **"Create new API key"** button
   - Enter a name: `Swavlamban 2025 System`
   - Copy the API key (looks like: `123456-1234-1234-1234-1234567890`)
   - **Save it securely** - you'll need it in the next step!

---

## Step 2: Configure Your System

### Option A: Using the `.env` File (Recommended)

1. **Open the `.env` file**:
   ```bash
   cd /home/santosh/Desktop/Swavlamban\ 2025/swavlamban2025/backend
   nano .env
   ```

2. **Add your MailBluster API key**:
   ```bash
   # Replace with your actual API key
   MAILBLUSTER_API_KEY=123456-1234-1234-1234-1234567890
   MAILBLUSTER_BRAND_ID=your-brand-id  # Optional
   USE_MAILBLUSTER=true
   ```

3. **Save the file** (Ctrl+O, Enter, Ctrl+X)

### Option B: Set Environment Variables (Alternative)

```bash
export MAILBLUSTER_API_KEY="your-api-key-here"
export USE_MAILBLUSTER=true
```

---

## Step 3: Connect SMTP Provider in MailBluster

Before you can send emails, you need to connect an SMTP provider in MailBluster:

1. **In MailBluster Dashboard**, click **"Connect provider"** under SMTP section
2. **Choose an SMTP provider**:
   - **Gmail** (Free - 500 emails/day)
   - **SendGrid** (Free tier available)
   - **Amazon SES** (Pay as you go)
   - **Or any other SMTP service**

3. **Follow the setup wizard** to connect your provider
4. **Verify your domain** (if required by the provider)

---

## Step 4: Test the Integration

### Quick Test from Streamlit UI:

1. **Login to your system**: http://localhost:8501
2. **Login as admin** (username: `admin`, password: `admin123`)
3. **Go to Admin Panel**
4. **Click "📧 Send Bulk Email"**
5. **Configure test email**:
   - Select "All Attendees" or a specific person
   - Write a test subject and message
   - Click "📤 Send Bulk Email"
6. **Check results** - You should see success/failure counts

### Test from Python:

```python
from backend.app.services.mailbluster_service import MailBlusterService

# Initialize service
email_service = MailBlusterService()

# Send test email
success = email_service.send_transactional_email(
    to_email="your-email@example.com",
    subject="Test Email from Swavlamban 2025",
    html_content="<h1>Hello!</h1><p>This is a test email.</p>",
    from_name="Swavlamban 2025 Team"
)

if success:
    print("✅ Email sent successfully!")
else:
    print("❌ Failed to send email")
```

---

## Step 5: Import Your Leads (Optional but Recommended)

To better manage your recipients in MailBluster:

### Method 1: Manual Import

1. **Go to MailBluster** → **Leads** → **Import leads**
2. **Export your attendees from Swavlamban system**:
   - Login as admin
   - Go to Admin Panel
   - Click "📥 Download All Entries (CSV)"
3. **Upload the CSV to MailBluster**
4. **Map columns**: Email → email, Name → firstName, etc.

### Method 2: Automatic Sync (Using API)

The system can automatically create leads when sending emails:

```python
# This happens automatically when using MailBlusterService
email_service.create_or_update_lead(
    email="attendee@example.com",
    first_name="John",
    last_name="Doe",
    subscribed=True,
    tags=["swavlamban-2025", "exhibition-day1"]
)
```

---

## 📊 Usage in the System

### From the Admin Panel (Bulk Emails):

1. **Login as admin**
2. **Admin Panel** → **Quick Actions**
3. **Click "📧 Send Bulk Email"**
4. **Select recipients**:
   - All Attendees
   - By Pass Type (Exhibition, Panel, Plenary)
   - By Organization
5. **Compose email** (subject + message)
6. **Optional**: Include QR code passes
7. **Send!**

### When Generating Passes (Individual Emails):

1. **Go to "Generate Passes"** tab
2. **Select attendee**
3. **Generate passes**
4. **Check "Send passes via email"**
5. **Click "Generate & Send Email"**
6. Attendee receives email with QR code passes attached!

---

## 🔧 Troubleshooting

### ❌ Error: "MailBluster API error: 401"

**Solution**: Your API key is incorrect or expired
- Check the API key in `.env` file
- Regenerate API key in MailBluster dashboard
- Update `.env` with new key
- Restart Streamlit: `streamlit run frontend/app.py`

### ❌ Error: "SMTP provider not connected"

**Solution**: Connect an SMTP provider in MailBluster
- Go to MailBluster → SMTP provider
- Click "Connect provider"
- Follow setup wizard

### ❌ Emails not sending

**Checklist**:
- ✅ API key configured in `.env`?
- ✅ SMTP provider connected in MailBluster?
- ✅ Email address verified?
- ✅ Not exceeding rate limits? (10 requests/second)
- ✅ Check MailBluster dashboard for sending status

### ❌ Attachments not showing

**Solution**: Pass files might be too large or incorrectly encoded
- Check pass files exist in `generated_passes/` directory
- Verify file size < 5MB per attachment
- Check MailBluster logs for attachment errors

---

## 📈 Rate Limits

MailBluster has the following limits:
- **10 requests per second**
- **100 requests per minute**

The system automatically handles these limits by:
- Sending emails sequentially (not all at once)
- Showing progress bar
- Reporting success/failure for each email

---

## 🎯 Advanced Features

### Create Email Campaigns (Alternative to Bulk Send)

Instead of using the system's bulk send, you can create campaigns in MailBluster:

1. **Export attendees** from Admin Panel (CSV)
2. **Import as leads** in MailBluster
3. **Create campaign** in MailBluster UI
4. **Design email** using MailBluster's editor
5. **Send to all leads or segments**

**Benefits**:
- Better email templates
- Analytics and tracking
- A/B testing
- Unsubscribe management

### Webhook Integration (Future Enhancement)

MailBluster supports webhooks for:
- Email opened
- Link clicked
- Email bounced
- Unsubscribed

You can add webhook endpoints to track email engagement!

---

## 📞 Support

### MailBluster Support:
- **Documentation**: https://developers.mailbluster.com
- **Support Email**: support@mailbluster.com
- **Dashboard**: https://app.mailbluster.com

### Swavlamban System Support:
- Check application logs
- Test API connection using Python script
- Verify environment variables are loaded

---

## ✅ Quick Setup Checklist

- [ ] Created MailBluster account
- [ ] Created/selected brand
- [ ] Generated API key
- [ ] Added API key to `.env` file
- [ ] Connected SMTP provider in MailBluster
- [ ] Verified sender email/domain
- [ ] Tested sending email from Admin Panel
- [ ] (Optional) Imported leads to MailBluster
- [ ] Ready to send emails! 🎉

---

## 🔐 Security Best Practices

1. **Never commit `.env` to Git** (already in `.gitignore`)
2. **Keep API key secret** - don't share publicly
3. **Rotate API keys regularly** (every 90 days)
4. **Use different API keys** for dev/staging/production
5. **Monitor usage** in MailBluster dashboard

---

## 📝 Example Email Templates

The system includes pre-built templates for:
- ✅ Exhibition Day 1 Pass
- ✅ Exhibition Day 2 Pass
- ✅ Panel Discussion Passes
- ✅ Plenary Session Pass

All templates are professionally designed with:
- Indian Navy branding
- Event details
- QR code attachments
- Support contact info

---

**Status**: ✅ Ready to use!
**Last Updated**: 2025-10-21
**Version**: 1.0

For any questions, refer to the MailBluster API documentation or test using the examples above.
