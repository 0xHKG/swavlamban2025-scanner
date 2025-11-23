#!/usr/bin/env python3
"""
Test NIC SMTP Email Service
Sends a test email to verify NIC SMTP configuration
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.services.nic_smtp_service import NICSmtpService

def test_nic_smtp():
    """Test NIC SMTP connection and send test email"""
    print("=" * 70)
    print("NIC SMTP TEST - Swavlamban 2025")
    print("=" * 70)

    # Initialize NIC SMTP service
    print("\n1. Initializing NIC SMTP service...")
    smtp_service = NICSmtpService()
    print(f"   ✅ Service initialized")
    print(f"   📧 Email: {smtp_service.sender_email}")
    print(f"   🖥️  Server: {smtp_service.smtp_server}:{smtp_service.smtp_port}")

    # Test connection
    print("\n2. Testing SMTP connection...")
    if not smtp_service.test_connection():
        print("   ❌ Connection test failed!")
        print("   Please check your credentials in backend/.env")
        return False

    # Send test email
    print("\n3. Sending test email...")
    recipient = "abhishekvardhan86@gmail.com"

    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #1D4E89;">✅ NIC SMTP Test - Swavlamban 2025</h2>

            <p>Dear User,</p>

            <p>This is a <strong>test email</strong> to verify that NIC SMTP integration is working correctly.</p>

            <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="color: #1D4E89;">📧 EMAIL SERVICE DETAILS:</h3>
                <ul style="list-style: none; padding-left: 0;">
                    <li>🖥️ <strong>SMTP Server:</strong> smtp.mgovcloud.in</li>
                    <li>🔐 <strong>Port:</strong> 587 (TLS)</li>
                    <li>📬 <strong>From:</strong> niio-tdac@navy.gov.in</li>
                    <li>✅ <strong>Status:</strong> Working!</li>
                </ul>
            </div>

            <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="color: #2e7d32;">✅ INTEGRATION SUCCESS</h3>
                <p>Your official Navy email (niio-tdac@navy.gov.in) is now configured and ready to send emails for Swavlamban 2025 event!</p>
            </div>

            <h3 style="color: #1D4E89;">Key Features Enabled:</h3>
            <ul>
                <li>✅ QR Code Pass Generation</li>
                <li>✅ Event Guidelines (DND) Attachments</li>
                <li>✅ Event Flow Schedule Attachments</li>
                <li>✅ Professional Navy Email Communication</li>
                <li>✅ Unlimited Daily Email Sending</li>
            </ul>

            <p style="margin-top: 30px;">If you received this email, the NIC SMTP integration is working perfectly!</p>

            <p style="margin-top: 30px;">For support: <a href="mailto:niio-tdac@navy.gov.in">niio-tdac@navy.gov.in</a></p>

            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
                <p style="color: #666; font-size: 14px;">
                    Best regards,<br>
                    <strong>Team Swavlamban 2025</strong><br>
                    Indian Navy | Innovation & Self-Reliance
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = """
NIC SMTP TEST - Swavlamban 2025

This is a test email to verify that NIC SMTP integration is working correctly.

EMAIL SERVICE DETAILS:
- SMTP Server: smtp.mgovcloud.in
- Port: 587 (TLS)
- From: niio-tdac@navy.gov.in
- Status: Working!

INTEGRATION SUCCESS
Your official Navy email (niio-tdac@navy.gov.in) is now configured and ready to send emails for Swavlamban 2025 event!

Key Features Enabled:
✅ QR Code Pass Generation
✅ Event Guidelines (DND) Attachments
✅ Event Flow Schedule Attachments
✅ Professional Navy Email Communication
✅ Unlimited Daily Email Sending

If you received this email, the NIC SMTP integration is working perfectly!

For support: niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy | Innovation & Self-Reliance
    """

    success = smtp_service.send_email(
        to_email=recipient,
        subject="✅ NIC SMTP Test - Swavlamban 2025",
        html_content=html_content,
        text_content=text_content,
        attachments=None
    )

    print("\n" + "=" * 70)
    if success:
        print("✅ TEST SUCCESSFUL!")
        print(f"📧 Test email sent to: {recipient}")
        print("📬 Check the inbox (and spam folder) for the test email")
        print("\n🎉 NIC SMTP is working correctly!")
        print("   You can now send emails from: niio-tdac@navy.gov.in")
    else:
        print("❌ TEST FAILED!")
        print("   Please check the error messages above")
    print("=" * 70)

    return success

if __name__ == "__main__":
    test_nic_smtp()
