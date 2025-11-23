#!/usr/bin/env python3
"""
Interactive NIC SMTP Test - Enter credentials manually
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_nic_smtp_interactive():
    """Test NIC SMTP with manual credential input"""
    print("=" * 70)
    print("NIC SMTP INTERACTIVE TEST - Swavlamban 2025")
    print("=" * 70)

    # Get credentials
    print("\nEnter your NIC SMTP credentials:")
    email_address = input("Email Address (e.g., niio-tdac@navy.gov.in): ").strip()
    password = input("Password (or App-Specific Password): ").strip()
    recipient = input("Test recipient email: ").strip() or "abhishekvardhan86@gmail.com"

    print(f"\n📊 Configuration:")
    print(f"   Server: smtp.mgovcloud.in:587")
    print(f"   Email: {email_address}")
    print(f"   Password length: {len(password)} characters")
    print(f"   Password starts with: {password[:4]}..." if len(password) > 4 else password)
    print(f"   Recipient: {recipient}")

    # Test connection
    print("\n🔄 Testing SMTP connection...")

    try:
        # Create test message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"Swavlamban 2025 <{email_address}>"
        msg['To'] = recipient
        msg['Subject'] = "✅ NIC SMTP Test - Swavlamban 2025"

        text_body = """
NIC SMTP TEST - Swavlamban 2025

This is a test email to verify NIC SMTP credentials.

If you receive this email, authentication is working correctly!

Server: smtp.mgovcloud.in:587
From: {email}

Best regards,
Swavlamban 2025 Team
""".format(email=email_address)

        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: #1D4E89;">✅ NIC SMTP Test - Swavlamban 2025</h2>
    <p>This is a test email to verify NIC SMTP credentials.</p>
    <p><strong>If you receive this email, authentication is working correctly!</strong></p>
    <div style="background: #f0f0f0; padding: 10px; margin: 20px 0;">
        <p><strong>Server:</strong> smtp.mgovcloud.in:587</p>
        <p><strong>From:</strong> {email_address}</p>
    </div>
    <p>Best regards,<br>Swavlamban 2025 Team</p>
</body>
</html>
"""

        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))

        # Connect and send
        print("📡 Connecting to smtp.mgovcloud.in:587...")
        with smtplib.SMTP('smtp.mgovcloud.in', 587) as server:
            print("🔒 Starting TLS encryption...")
            server.set_debuglevel(1)  # Show SMTP debug output
            server.starttls()

            print(f"🔑 Authenticating as {email_address}...")
            server.login(email_address, password)

            print(f"📧 Sending test email to {recipient}...")
            server.send_message(msg)

        print("\n" + "=" * 70)
        print("✅ SUCCESS! Email sent successfully!")
        print(f"📧 Check {recipient} inbox (and spam folder)")
        print("=" * 70)
        return True

    except smtplib.SMTPAuthenticationError as e:
        print("\n" + "=" * 70)
        print("❌ AUTHENTICATION FAILED!")
        print(f"Error: {e}")
        print("\nPossible issues:")
        print("1. ❌ Wrong password")
        print("2. ❌ 2FA enabled - need Application-Specific Password")
        print("3. ❌ Wrong email format (should be full email: user@navy.gov.in)")
        print("\nTo generate App-Specific Password:")
        print("   1. Login to https://mail.gov.in")
        print("   2. Settings → Security")
        print("   3. Generate Application-Specific Password")
        print("=" * 70)
        return False

    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERROR!")
        print(f"Error: {e}")
        print("=" * 70)
        return False

if __name__ == "__main__":
    test_nic_smtp_interactive()
