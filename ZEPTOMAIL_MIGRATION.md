# ZeptoMail Migration Plan

**Date:** 2025-11-05
**Status:** ⏳ PENDING ACCOUNT VERIFICATION
**Current Provider:** Mailjet (payment issues)
**New Provider:** ZeptoMail (Zoho)

---

## 📋 Migration Context

### Issue with Current Provider:
- **Mailjet**: Payment processing not working
- **Need**: Alternative email service provider for sending passes to 76 seminar attendees

### Selected Alternative:
- **Provider**: ZeptoMail by Zoho
- **Reason**: Reliable transactional email service with good pricing

---

## 🔍 ZeptoMail Account Status

### Current Status (2025-11-05):
**Account Status:** ⏳ Under Review

The modal shown in ZeptoMail dashboard states:
```
Account not reviewed

We review every new account created in ZeptoMail to ensure that the usage
is compatible with our service.

Your account is in the review phase and it can take up to 2-3 business days
from the KYC submission, for the process to be completed. You can reach out
to us via chat for further clarification.
```

### Domain Setup:
- **Domain**: swavlamban2025.streamlit.app
- **Status**: Pending (DNS records to be verified after account approval)
- **Mail Agent**: mail_agent_1 (created on 05 Nov 2025)

### DKIM/CNAME Records Status:
- **DKIM**: Pending verification
- **CNAME (bounce)**: Pending verification

---

## 💰 ZeptoMail Pricing Analysis

### Pricing Model:
- **Type**: Pay-as-you-go (credit-based)
- **1 Credit**: 10,000 emails
- **Cost**: $2.50 per credit (varies by currency)
- **Validity**: 6 months from purchase
- **Free Tier**: 10,000 emails (1 credit) - FREE

### For Our Use Case (76 Seminar Attendees):
- **Immediate Need**: 76 emails
- **Buffer**: ~100-150 emails (for resends/corrections)
- **Cost**: $0 (covered by free tier)

### Key Benefits:
✅ **No daily sending limits** (unlike Mailjet Free: 200/day)
✅ **No monthly commitments**
✅ **Pay only for what you use**
✅ **10,000 free emails to start**
✅ **Credits valid for 6 months**
✅ **All features available regardless of volume**

### Comparison with Mailjet:

| Feature | Mailjet Free | Mailjet Essential | ZeptoMail Free |
|---------|--------------|-------------------|----------------|
| Monthly Emails | 6,000 | 15,000 | 10,000 (one-time) |
| Daily Limit | 200/day | No limit | No limit |
| Cost | $0 | $17/month | $0 (then $2.50/10k) |
| Logo in Email | Yes | No | No |
| Support | Community | Online | Chat support |

---

## 🔧 Technical Integration

### Current Email Service Architecture:

**Priority Order (email_service.py):**
1. Mailjet API (if credentials set)
2. NIC SMTP (if enabled)
3. Gmail SMTP (if enabled)
4. MailBluster (if API key set)

### Required Changes for ZeptoMail:

#### 1. Create ZeptoMail Service File:
**File**: `backend/app/services/zeptomail_service.py`

```python
"""
ZeptoMail API service for transactional emails
"""
import requests
from pathlib import Path
from typing import List, Optional
import base64

from ..core.config import settings


class ZeptoMailService:
    """Email service using ZeptoMail API"""

    def __init__(self):
        self.api_key = settings.ZEPTOMAIL_API_KEY
        self.api_url = "https://api.zeptomail.com/v1.1/email"
        self.from_email = settings.EMAIL_SENDER  # niio-tdac@navy.gov.in
        self.from_name = "Team Swavlamban 2025"

    def send_email(self, to_email: str, subject: str,
                   html_content: str, text_content: str = None,
                   attachments: List[Path] = None) -> bool:
        """Send email via ZeptoMail API"""

        headers = {
            "Authorization": f"Zoho-enczapikey {self.api_key}",
            "Content-Type": "application/json"
        }

        # Prepare attachments
        email_attachments = []
        if attachments:
            for attachment_path in attachments:
                if not attachment_path.exists():
                    continue

                with open(attachment_path, "rb") as f:
                    file_data = base64.b64encode(f.read()).decode()

                email_attachments.append({
                    "content": file_data,
                    "name": attachment_path.name
                })

        # Build email payload
        payload = {
            "from": {
                "address": self.from_email,
                "name": self.from_name
            },
            "to": [
                {
                    "email_address": {
                        "address": to_email
                    }
                }
            ],
            "subject": subject,
            "htmlbody": html_content,
        }

        if text_content:
            payload["textbody"] = text_content

        if email_attachments:
            payload["attachments"] = email_attachments

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                return True
            else:
                print(f"ZeptoMail error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"ZeptoMail exception: {e}")
            return False
```

#### 2. Update Email Service Priority:
**File**: `backend/app/services/email_service.py`

Add ZeptoMail as first priority (lines 164-171):

```python
# 1. ZeptoMail API (Transactional email service - FAST)
if settings.ZEPTOMAIL_API_KEY:
    from .zeptomail_service import ZeptoMailService
    self.provider = ZeptoMailService()
    self.provider_name = "ZeptoMail API"
    self.uses_smtp = False  # Uses API with base64 attachments
    print("✅ Using ZeptoMail API (Transactional email)")
# 2. Mailjet API (if configured)
elif settings.MAILJET_API_KEY and settings.MAILJET_API_SECRET:
    ...
```

#### 3. Add Configuration:
**File**: `backend/app/core/config.py`

```python
# ZeptoMail API
ZEPTOMAIL_API_KEY: Optional[str] = None
```

#### 4. Update Environment Variables:
**File**: `backend/.env` (local) and Streamlit Secrets (production)

```toml
# ZeptoMail API (Primary email provider)
ZEPTOMAIL_API_KEY = "your-zeptomail-api-key-here"
```

#### 5. Update Requirements:
**File**: `frontend/requirements.txt`

```
requests==2.31.0  # Already included
```

---

## 📝 Migration Steps

### Phase 1: Account Approval ⏳ IN PROGRESS
- [x] Create ZeptoMail account
- [x] Submit domain for verification
- [x] Contact customer care for review
- [ ] **Wait 2-3 business days** for account approval
- [ ] Verify account status changes from "Pending" to "Active"

### Phase 2: Domain Verification ⏳ PENDING
After account approval:
- [ ] Add DNS records (DKIM, CNAME) provided by ZeptoMail
- [ ] Verify domain ownership
- [ ] Confirm bounce handling setup

### Phase 3: API Integration ⏳ PENDING
- [ ] Get API key from ZeptoMail dashboard (Settings → API)
- [ ] Create `zeptomail_service.py` file
- [ ] Update `email_service.py` with ZeptoMail priority
- [ ] Update `config.py` with ZEPTOMAIL_API_KEY
- [ ] Add API key to Streamlit Cloud secrets

### Phase 4: Testing 📋 TODO
- [ ] Test single email sending
- [ ] Test email with attachments (QR passes)
- [ ] Test with multiple attachments (4-6 files)
- [ ] Verify email delivery
- [ ] Check inbox placement (not spam)
- [ ] Test with 5-10 real attendees

### Phase 5: Production Deployment 🚀 TODO
- [ ] Commit code changes to GitHub
- [ ] Push to production
- [ ] Reboot Streamlit Cloud app
- [ ] Verify ZeptoMail initialized correctly in logs
- [ ] Send passes to all 76 seminar attendees
- [ ] Monitor sending success rate

---

## 📊 Expected Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Account Approval | 2-3 business days | ⏳ In Progress |
| Domain Verification | 1 hour | ⏳ Pending |
| API Integration | 2-3 hours | ⏳ Pending |
| Testing | 1-2 hours | ⏳ Pending |
| Production Deploy | 30 minutes | ⏳ Pending |
| **TOTAL** | **3-4 business days** | **~60% Complete** |

---

## 🎯 Success Criteria

### Must Have:
- ✅ Account approved by ZeptoMail
- ✅ Domain verified and active
- ✅ API integration working
- ✅ Emails delivered successfully
- ✅ QR pass attachments working (4-6 files per email)
- ✅ All 76 attendees receive passes

### Nice to Have:
- ✅ Email delivery < 10 seconds per email
- ✅ 100% inbox placement (not spam)
- ✅ Detailed delivery tracking

---

## 🚨 Rollback Plan

If ZeptoMail doesn't work:

### Alternative 1: Fix Mailjet Payment
- Retry payment with different card
- Use PayPal instead
- Contact Mailjet support

### Alternative 2: Use NIC SMTP
- Already configured: niio-tdac@navy.gov.in
- Status: Working (tested)
- Limitation: Slow (90s per email)
- Total time: ~114 minutes for 76 emails

### Alternative 3: Use Gmail SMTP
- Already configured: Swavlamban2025@gmail.com
- Status: Working (tested)
- Limitation: 500 emails/day
- Sufficient for 76 emails

---

## 📞 Support Contacts

### ZeptoMail Support:
- **Chat**: Available in dashboard
- **Help Portal**: https://help.zoho.com/portal/en/kb/zeptomail
- **API Docs**: https://www.zoho.com/zeptomail/help/api-home.html

### Internal Contacts:
- **Admin**: abhishekvardhan86@gmail.com
- **TDAC Support**: niio-tdac@navy.gov.in | 011-26771528

---

## 📚 References

### Documentation:
- ZeptoMail Pricing: https://www.zoho.com/zeptomail/pricing.html
- API Documentation: https://www.zoho.com/zeptomail/help/api/email-sending.html
- FAQ: https://help.zoho.com/portal/en/kb/zeptomail/faqs

### Internal Files:
- Email Service: `backend/app/services/email_service.py`
- Pass Generator: `backend/app/services/pass_generator.py`
- Config: `backend/app/core/config.py`

---

## ✅ Current Status Summary

**Account Status:** ⏳ Under Review (2-3 business days)
**Next Action:** Wait for account approval notification
**Estimated Ready Date:** 2025-11-07 or 2025-11-08
**Blocker:** Account verification by ZeptoMail team

**Once Approved:**
1. Verify domain with DNS records
2. Get API key
3. Integrate code (2-3 hours)
4. Test and deploy
5. Send passes to 76 attendees

---

**Last Updated:** 2025-11-05
**Document Owner:** Claude + User
**Status:** Living document (update as migration progresses)
