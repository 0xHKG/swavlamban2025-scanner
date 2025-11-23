#!/usr/bin/env python3
"""
Test NIC SMTP with SSL (Port 465)
"""
import sys
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))
from app.core.config import settings

def test_with_ssl():
    """Test NIC SMTP using SSL (port 465)"""
    print("=" * 70)
    print("NIC SMTP TEST - SSL (Port 465)")
    print("=" * 70)

    smtp_server = "smtp.mgovcloud.in"
    smtp_port = 465
    email = settings.NIC_EMAIL_ADDRESS
    password = settings.NIC_EMAIL_PASSWORD

    print(f"\n📧 Email: {email}")
    print(f"🖥️  Server: {smtp_server}:{smtp_port}")
    print(f"🔐 Password length: {len(password)} chars")

    try:
        print("\n1. Connecting via SSL...")
        # Use SMTP_SSL for port 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        print("   ✅ SSL connection established")

        print("\n2. Logging in...")
        server.login(email, password)
        print("   ✅ Authentication successful!")

        print("\n3. Sending test email...")
        msg = MIMEMultipart()
        msg['From'] = f"Swavlamban 2025 <{email}>"
        msg['To'] = "abhishekvardhan86@gmail.com"
        msg['Subject'] = "✅ NIC SMTP Test (SSL) - Swavlamban 2025"

        body = """
This is a test email sent via NIC SMTP using SSL (port 465).

If you received this, the NIC SMTP integration is working!

Server: smtp.mgovcloud.in
Port: 465 (SSL)
From: niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy
        """

        msg.attach(MIMEText(body, 'plain'))
        server.send_message(msg)
        print("   ✅ Email sent successfully!")

        server.quit()

        print("\n" + "=" * 70)
        print("✅ SSL TEST SUCCESSFUL!")
        print("📧 Email sent to: abhishekvardhan86@gmail.com")
        print("📬 Check inbox (and spam folder)")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n" + "=" * 70)
        print("❌ SSL TEST FAILED")
        print("=" * 70)
        return False

if __name__ == "__main__":
    test_with_ssl()
