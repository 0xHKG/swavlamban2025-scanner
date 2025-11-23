#!/usr/bin/env python3
"""
Standalone Test Script for Brevo Email Integration
Sends a test email with attachment to verify Brevo API is working correctly
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Check if sib-api-v3-sdk is installed
try:
    import sib_api_v3_sdk
    from sib_api_v3_sdk.rest import ApiException
except ImportError:
    print("❌ Error: sib-api-v3-sdk not installed")
    print("\n📦 Install with: pip install sib-api-v3-sdk")
    print("   Or: pip install -r backend/requirements.txt")
    sys.exit(1)

import base64
import time
from datetime import datetime


def send_test_email_with_attachment():
    """Send test email using Brevo API with attachment"""

    print("=" * 70)
    print("🧪 BREVO API TEST - Email with Attachment")
    print("=" * 70)

    # Configuration (REPLACE WITH YOUR ACTUAL API KEY)
    BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
    SENDER_EMAIL = "swavlamban2025@gmail.com"
    SENDER_NAME = "Swavlamban 2025 - Test"
    RECIPIENT_EMAIL = "abhishekvardhan86@gmail.com"

    if not BREVO_API_KEY:
        print("\n❌ Error: BREVO_API_KEY not found!")
        print("\n📋 Setup instructions:")
        print("   1. Get your API key from: https://app.brevo.com/settings/keys/api")
        print("   2. Set environment variable:")
        print("      export BREVO_API_KEY='your-api-key-here'")
        print("   3. Or add to .env file:")
        print("      BREVO_API_KEY=your-api-key-here")
        return False

    print(f"\n📧 Test Email Configuration:")
    print(f"   Sender: {SENDER_NAME} <{SENDER_EMAIL}>")
    print(f"   Recipient: {RECIPIENT_EMAIL}")
    print(f"   API Key: {BREVO_API_KEY[:10]}...{BREVO_API_KEY[-10:]}")

    try:
        # Configure API client
        print("\n🔧 Configuring Brevo API client...")
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        print("   ✅ API client configured")

        # Create test attachment file
        print("\n📎 Creating test attachment...")
        attachment_file = Path("brevo_test_attachment.txt")
        attachment_content = f"""
Brevo API Integration Test
===========================

Test performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Email service: Brevo (formerly Sendinblue)
Sender: {SENDER_EMAIL}
Recipient: {RECIPIENT_EMAIL}

Integration Details:
-------------------
- API: Brevo REST API v3
- SDK: sib-api-v3-sdk (Python)
- Project: Swavlamban 2025
- Purpose: Pass distribution system for Indian Navy event

This is a test attachment to verify that:
1. Brevo API authentication works
2. Email sending is functional
3. File attachments are properly encoded and transmitted
4. HTML email rendering is correct

If you received this email with this attachment, the integration is successful! ✅

---
Indian Navy | Innovation & Self-Reliance
Swavlamban 2025
"""
        attachment_file.write_text(attachment_content)
        print(f"   ✅ Created: {attachment_file.name}")

        # Read and encode attachment
        print("\n🔄 Encoding attachment to base64...")
        with open(attachment_file, 'rb') as f:
            file_data = f.read()
            encoded_string = base64.b64encode(file_data)
            base64_content = encoded_string.decode('utf-8')
        print(f"   ✅ Encoded {len(file_data)} bytes → {len(base64_content)} base64 chars")

        # Prepare email content
        print("\n✍️  Preparing email content...")
        subject = f"Brevo Integration Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #003366 0%, #0066cc 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .content {{
            background: #f8f9fa;
            padding: 30px;
            border-left: 4px solid #003366;
            border-right: 4px solid #003366;
        }}
        .success-box {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .info-box {{
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .details {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        .details strong {{
            color: #003366;
        }}
        .footer {{
            background: #003366;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 0 0 10px 10px;
            font-size: 12px;
        }}
        .attachment-notice {{
            background: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Brevo API Integration Test</h1>
        <p style="margin: 5px 0 0 0;">Swavlamban 2025</p>
    </div>

    <div class="content">
        <div class="success-box">
            <strong>✅ Email Successfully Sent!</strong><br>
            If you're reading this, the Brevo API integration is working correctly.
        </div>

        <h2 style="color: #003366;">Test Details</h2>
        <div class="details">
            <p><strong>Test Time:</strong> {datetime.now().strftime('%d %B %Y, %H:%M:%S IST')}</p>
            <p><strong>Email Service:</strong> Brevo (formerly Sendinblue)</p>
            <p><strong>API Version:</strong> REST API v3</p>
            <p><strong>Python SDK:</strong> sib-api-v3-sdk</p>
            <p><strong>Sender:</strong> {SENDER_EMAIL}</p>
            <p><strong>Recipient:</strong> {RECIPIENT_EMAIL}</p>
        </div>

        <div class="info-box">
            <strong>📋 Integration Purpose</strong><br>
            This test verifies the Brevo API integration for the Swavlamban 2025 event
            registration system. The system will use Brevo to send event passes with QR
            codes to registered attendees.
        </div>

        <div class="attachment-notice">
            <strong>📎 Attachment Included</strong><br>
            This email includes a test text file attachment (<code>{attachment_file.name}</code>)
            to verify that file attachments work correctly. Please check if you received the attachment.
        </div>

        <h2 style="color: #003366;">Features Tested</h2>
        <ul>
            <li>✅ API Authentication</li>
            <li>✅ HTML Email Rendering</li>
            <li>✅ File Attachment (Base64 encoding)</li>
            <li>✅ Custom Sender Information</li>
            <li>✅ Transactional Email Delivery</li>
        </ul>

        <h2 style="color: #003366;">Priority Configuration</h2>
        <p>The email system is configured with the following priority:</p>
        <ol>
            <li><strong>Brevo API</strong> (PRIMARY) - Fast transactional email</li>
            <li><strong>Mailjet API</strong> (STANDBY) - Fallback if Brevo fails</li>
            <li><strong>Gmail SMTP</strong> (FINAL FALLBACK) - Last resort</li>
        </ol>
    </div>

    <div class="footer">
        <p style="margin: 0;"><strong>Swavlamban 2025</strong></p>
        <p style="margin: 5px 0;">Indian Navy | Innovation & Self-Reliance</p>
        <p style="margin: 5px 0; font-size: 10px;">Event Date: 25-26 November 2025 | Venue: Manekshaw Centre</p>
    </div>
</body>
</html>
"""

        # Prepare sender and recipient
        sender = {
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        }

        to = [{"email": RECIPIENT_EMAIL}]

        # Prepare attachment
        attachment = [{
            "content": base64_content,
            "name": attachment_file.name
        }]

        # Create email object
        print("   ✅ Email content prepared")
        print(f"   Subject: {subject}")
        print(f"   HTML content: {len(html_content)} characters")
        print(f"   Attachment: {attachment_file.name} ({len(file_data)} bytes)")

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            subject=subject,
            html_content=html_content,
            attachment=attachment
        )

        # Send email
        print("\n📤 Sending email via Brevo API...")
        start_time = time.time()

        api_response = api_instance.send_transac_email(send_smtp_email)

        send_time = time.time() - start_time

        # Success!
        print("\n" + "=" * 70)
        print("✅ SUCCESS! Email sent successfully via Brevo API")
        print("=" * 70)
        print(f"\n📊 Delivery Details:")
        print(f"   Message ID: {api_response.message_id if hasattr(api_response, 'message_id') else 'N/A'}")
        print(f"   Send time: {send_time:.2f} seconds")
        print(f"   Recipient: {RECIPIENT_EMAIL}")
        print(f"   Subject: {subject}")
        print(f"   Attachment: {attachment_file.name}")

        print(f"\n💡 Next Steps:")
        print(f"   1. Check inbox at {RECIPIENT_EMAIL}")
        print(f"   2. Verify HTML rendering is correct")
        print(f"   3. Confirm attachment is received")
        print(f"   4. Update .env or Streamlit secrets with BREVO_API_KEY")

        # Cleanup test file
        attachment_file.unlink()
        print(f"\n🧹 Cleaned up test file: {attachment_file.name}")

        return True

    except ApiException as e:
        print(f"\n❌ Brevo API Error:")
        print(f"   Status: {e.status if hasattr(e, 'status') else 'Unknown'}")
        print(f"   Reason: {e.reason if hasattr(e, 'reason') else 'Unknown'}")
        print(f"   Body: {e.body if hasattr(e, 'body') else 'No details'}")

        # Cleanup test file
        if Path("brevo_test_attachment.txt").exists():
            Path("brevo_test_attachment.txt").unlink()

        return False

    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()

        # Cleanup test file
        if Path("brevo_test_attachment.txt").exists():
            Path("brevo_test_attachment.txt").unlink()

        return False


if __name__ == "__main__":
    print("\n🚀 Starting Brevo API Test...")
    print("   This will send a test email with attachment to abhishekvardhan86@gmail.com\n")

    success = send_test_email_with_attachment()

    if success:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed. Please check the error messages above.")
        sys.exit(1)
