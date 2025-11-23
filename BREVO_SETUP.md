# Brevo API Setup Guide

**Status**: ✅ INTEGRATED & READY FOR TESTING
**Service**: Brevo (formerly Sendinblue)
**Priority**: PRIMARY email service
**API**: REST API v3
**SDK**: sib-api-v3-sdk 7.6.0

---

## Overview

Brevo (formerly Sendinblue) is now the **PRIMARY** email service for the Swavlamban 2025 event registration system. It provides:

- **Fast delivery**: ~10 seconds per email (vs ~90s for SMTP)
- **REST API**: Modern API-based sending (vs slow SMTP protocol)
- **Free tier**: 300 emails/day included
- **Reliable**: Professional transactional email service
- **Attachments**: Full support for QR passes, DND images, Event Flow PDFs

### Email Provider Priority Order

1. **Brevo API** (PRIMARY) - Fast transactional email ⚡
2. **Mailjet API** (STANDBY) - Fallback if Brevo fails
3. **Gmail SMTP** (FINAL FALLBACK) - Last resort if both APIs fail
4. NIC SMTP (Optional - for government email)
5. MailBluster (Optional - alternative)

---

## Step 1: Create Brevo Account

1. Go to https://app.brevo.com
2. Sign up for a free account (or login if you already have one)
3. Verify your email address
4. Complete account setup

**Free Tier Limits**:
- 300 emails/day
- Unlimited contacts
- Email API access
- Transactional emails included

---

## Step 2: Add Sender Email

Before sending emails, you must verify `swavlamban2025@gmail.com` as a sender:

1. Go to **Settings** → **Senders & IP**
2. Click **Add a sender**
3. Enter:
   - **Email**: `swavlamban2025@gmail.com`
   - **Name**: `Swavlamban 2025`
4. Click **Save**
5. Check the Gmail inbox for verification email
6. Click verification link in email
7. Wait for "Verified" status in Brevo dashboard

**Important**: You cannot send emails until the sender is verified!

---

## Step 3: Generate API Key

1. Go to **Settings** → **API Keys** (or visit https://app.brevo.com/settings/keys/api)
2. Click **Generate a new API key**
3. Enter name: `Swavlamban 2025 Production`
4. Copy the API key (it will only be shown once!)
5. Save it securely

**Example API Key format**: `xkeysib-a1b2c3d4e5f6...`

---

## Step 4: Configure Application

### For Local Development (.env file)

Add to `backend/.env`:

```bash
# Email - Brevo (PRIMARY)
BREVO_API_KEY=xkeysib-your-actual-api-key-here
USE_BREVO=true
```

### For Streamlit Cloud (Secrets)

Go to Streamlit Cloud → Settings → Secrets and add:

```toml
# Email - Brevo (PRIMARY - formerly Sendinblue)
BREVO_API_KEY = "xkeysib-your-actual-api-key-here"
USE_BREVO = true

# Email - Mailjet (STANDBY - fallback if Brevo fails)
MAILJET_API_KEY = "your-mailjet-key"
MAILJET_API_SECRET = "your-mailjet-secret"

# Email - Gmail SMTP (FINAL FALLBACK)
GMAIL_ADDRESS = "Swavlamban2025@gmail.com"
GMAIL_APP_PASSWORD = "pwiwmzgshilvmeon"
USE_GMAIL_SMTP = true
```

---

## Step 5: Install Dependencies

The Brevo Python SDK is already included in `backend/requirements.txt`:

```bash
sib-api-v3-sdk==7.6.0  # Brevo API (PRIMARY)
```

To install locally:

```bash
cd backend
pip install -r requirements.txt
```

Or install just the Brevo SDK:

```bash
pip install sib-api-v3-sdk==7.6.0
```

---

## Step 6: Test Integration

### Option A: Standalone Test Script

Use the provided test script to verify Brevo integration:

```bash
# Set API key
export BREVO_API_KEY='xkeysib-your-actual-api-key-here'

# Run test script
python test_brevo_email.py
```

This will:
- Send test email to `abhishekvardhan86@gmail.com`
- Include a test attachment (`brevo_test_attachment.txt`)
- Display detailed HTML email with all features
- Show timing information
- Verify API authentication works

**Expected Output**:
```
==================================================
🧪 BREVO API TEST - Email with Attachment
==================================================

📧 Test Email Configuration:
   Sender: Swavlamban 2025 - Test <swavlamban2025@gmail.com>
   Recipient: abhishekvardhan86@gmail.com
   API Key: xkeysib-a1...********

🔧 Configuring Brevo API client...
   ✅ API client configured

📎 Creating test attachment...
   ✅ Created: brevo_test_attachment.txt

🔄 Encoding attachment to base64...
   ✅ Encoded 1024 bytes → 1368 base64 chars

✍️  Preparing email content...
   ✅ Email content prepared
   Subject: Brevo Integration Test - 2025-11-06 10:30
   HTML content: 3456 characters
   Attachment: brevo_test_attachment.txt (1024 bytes)

📤 Sending email via Brevo API...

==================================================
✅ SUCCESS! Email sent successfully via Brevo API
==================================================

📊 Delivery Details:
   Message ID: <abc123xyz@smtp-relay.brevo.com>
   Send time: 8.45 seconds
   Recipient: abhishekvardhan86@gmail.com
   Subject: Brevo Integration Test - 2025-11-06 10:30
   Attachment: brevo_test_attachment.txt

💡 Next Steps:
   1. Check inbox at abhishekvardhan86@gmail.com
   2. Verify HTML rendering is correct
   3. Confirm attachment is received
   4. Update .env or Streamlit secrets with BREVO_API_KEY

🧹 Cleaned up test file: brevo_test_attachment.txt

✅ Test completed successfully!
```

### Option B: Test via Streamlit App

1. Start the backend:
```bash
cd backend
python -m app.main
```

2. Start the frontend:
```bash
cd frontend
streamlit run app.py
```

3. Login and generate passes for a test entry
4. Click "📧 Generate Passes & Send Email"
5. Check console output for "✅ Using Brevo API (PRIMARY - fast transactional email)"

---

## How It Works

### Architecture

```
Streamlit App (frontend/app.py)
    ↓
EmailService (backend/app/services/email_service.py)
    ↓
Priority Check:
    1. Brevo API available? → Use BrevoService
    2. Mailjet API available? → Use MailjetService
    3. Gmail SMTP available? → Use GmailSMTPService
    4. Fallback to other providers...
```

### BrevoService Implementation

File: `backend/app/services/brevo_service.py`

```python
class BrevoService:
    def __init__(self):
        # Initialize Brevo API client
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = settings.BREVO_API_KEY
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(self.configuration)
        )

    def send_email(self, to_email, subject, html_content,
                   text_content="", attachments=None):
        # Base64 encode attachments
        brevo_attachments = []
        for file_path in attachments:
            with open(file_path, 'rb') as f:
                base64_content = base64.b64encode(f.read()).decode('utf-8')
            brevo_attachments.append({
                "content": base64_content,
                "name": Path(file_path).name
            })

        # Create email
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"name": "Swavlamban 2025", "email": self.sender_email},
            subject=subject,
            html_content=html_content,
            attachment=brevo_attachments if brevo_attachments else None
        )

        # Send via Brevo API
        api_response = self.api_instance.send_transac_email(send_smtp_email)
        return True
```

### Attachment Support

Brevo API supports attachments in base64 format:

**Supported formats**: xlsx, xls, ods, docx, doc, csv, pdf, txt, gif, jpg, jpeg, png, tif, tiff, rtf, bmp, zip, xml, ppt, pptx

**Current attachments**:
- **QR Passes**: EP-25.png, EP-26.png, EP-INTERACTIVE.png, EP-PLENARY.png (~650-900 KB each)
- **DND Images**: DND_Exhibition.png, DND_Interactive.png, DND_Plenary.png (~700-800 KB each)
- **Event Flow**: EF-25.png, EF-AM26.png, EF-PM26.png (~600-620 KB each)

**Total per email**: 2-4 MB (depending on number of passes)

---

## Troubleshooting

### Issue: "Authentication error" or 401 Unauthorized

**Cause**: Invalid or missing API key

**Solution**:
1. Check API key is set in environment: `echo $BREVO_API_KEY`
2. Verify API key in Brevo dashboard (Settings → API Keys)
3. Ensure no extra spaces or quotes in .env file
4. Regenerate API key if necessary

### Issue: "Sender email not verified"

**Cause**: swavlamban2025@gmail.com not verified as sender

**Solution**:
1. Go to Settings → Senders & IP in Brevo dashboard
2. Check status of swavlamban2025@gmail.com
3. If not verified, click "Resend verification email"
4. Check Gmail inbox and click verification link

### Issue: "Daily sending limit exceeded"

**Cause**: Free tier limit of 300 emails/day reached

**Solution**:
1. Wait until tomorrow (limit resets at midnight UTC)
2. Or upgrade to paid plan for higher limits
3. System will automatically fallback to Mailjet → Gmail SMTP

### Issue: Email not received

**Check**:
1. Look in spam/junk folder
2. Check Brevo dashboard → Campaigns → Transactional emails → Email logs
3. Verify recipient email is correct
4. Check test script output for message ID

### Issue: "ApiException" error

**Cause**: Various API errors (rate limit, invalid params, etc.)

**Solution**:
1. Check error message in exception: `e.body`
2. Check Brevo API status: https://status.brevo.com
3. Verify all required fields are provided
4. Check API documentation: https://developers.brevo.com

---

## API Rate Limits

### Free Tier
- **300 emails/day**
- **Unlimited contacts**
- **Rate limit**: 300 requests/minute

### Lite Plan ($25/month)
- **10,000 emails/month**
- **All features included**
- **No daily limit**

### Premium Plan ($65/month)
- **20,000 emails/month**
- **Advanced features**
- **Priority support**

**For Swavlamban 2025**: Free tier (300/day) should be sufficient for most use cases. If you need to send more, system will fallback to Mailjet and Gmail SMTP.

---

## Monitoring & Analytics

Brevo provides detailed analytics:

1. Go to **Campaigns** → **Transactional emails**
2. View:
   - Total emails sent
   - Delivery rate
   - Open rate (if tracking enabled)
   - Click rate (if tracking enabled)
   - Bounce rate
   - Spam complaints

**Email logs**: See individual email status (sent, delivered, opened, clicked, bounced, etc.)

---

## Comparison: Brevo vs SMTP

| Feature | Brevo API | SMTP (Gmail/NIC) |
|---------|-----------|------------------|
| **Speed** | ~10s per email | ~90s per email |
| **Protocol** | REST API (HTTPS) | SMTP (TCP) |
| **Attachments** | Base64 in JSON | MIME multipart |
| **Reliability** | High (dedicated service) | Medium (shared servers) |
| **Daily Limit** | 300 (free), 10K+ (paid) | 500 (Gmail), unlimited (NIC) |
| **Setup** | API key only | Password + geo-fencing (NIC) |
| **Cost** | $0 (free tier) | $0 |

**Recommendation**: Use Brevo API as primary for speed and reliability. Keep SMTP as fallback for redundancy.

---

## Security Best Practices

1. **Never commit API keys to Git**
   - Always use environment variables or secrets
   - Add `.env` to `.gitignore`

2. **Rotate API keys regularly**
   - Generate new key every 3-6 months
   - Delete old keys from Brevo dashboard

3. **Use separate keys for dev/prod**
   - Create "Development" and "Production" API keys
   - Limit dev key permissions if possible

4. **Monitor usage**
   - Check Brevo dashboard regularly
   - Set up alerts for suspicious activity

5. **Verify sender emails**
   - Only use verified sender addresses
   - Don't send from unverified domains

---

## Additional Resources

- **Brevo Website**: https://www.brevo.com
- **Brevo Dashboard**: https://app.brevo.com
- **API Documentation**: https://developers.brevo.com
- **Python SDK Docs**: https://github.com/sendinblue/APIv3-python-library
- **API Status**: https://status.brevo.com
- **Support**: support@brevo.com

---

## Next Steps

1. ✅ Create Brevo account
2. ✅ Verify sender email (swavlamban2025@gmail.com)
3. ✅ Generate API key
4. ✅ Configure application (.env or Streamlit secrets)
5. ✅ Install dependencies (sib-api-v3-sdk)
6. ⏳ Run test script (`python test_brevo_email.py`)
7. ⏳ Verify test email received
8. ⏳ Test via Streamlit app with real pass generation
9. ⏳ Deploy to production with Brevo configured
10. ⏳ Monitor email delivery and analytics

---

**Document Version**: 1.0
**Last Updated**: 2025-11-06
**Status**: ✅ INTEGRATED & READY FOR TESTING
