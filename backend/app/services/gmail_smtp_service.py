"""
Gmail SMTP Integration Service
Free email sending using Gmail SMTP (no third-party service required)
"""
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional

from ..core.config import settings


class GmailSMTPService:
    """Service for sending emails via Gmail SMTP (completely FREE)"""

    def __init__(self):
        """Initialize Gmail SMTP service"""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # TLS
        self.sender_email = settings.GMAIL_ADDRESS
        self.sender_password = settings.GMAIL_APP_PASSWORD

    def send_email(self, to_email: str, subject: str, html_content: str,
                   text_content: str = "", attachments: List[str] = None) -> bool:
        """
        Send email via Gmail SMTP

        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)
            attachments: List of file paths to attach

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"Swavlamban 2025 <{self.sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)

            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)

            # Add attachments
            if attachments:
                for file_path in attachments:
                    if Path(file_path).exists():
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={Path(file_path).name}'
                            )
                            msg.attach(part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"✅ Email sent successfully to {to_email}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False

    def send_bulk_email(self, recipients: List[str], subject: str,
                       html_content: str, text_content: str = "",
                       attachments: List[str] = None) -> dict:
        """
        Send bulk emails to multiple recipients
        Uses PERSISTENT CONNECTION for faster bulk sending

        Args:
            recipients: List of email addresses
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body
            attachments: List of file paths to attach

        Returns:
            dict: {"success": count, "failed": count}
        """
        results = {"success": 0, "failed": 0}

        try:
            # OPTIMIZATION: Reuse single SMTP connection for all emails
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                print(f"✅ Connected to Gmail SMTP for bulk sending ({len(recipients)} emails)")

                for email in recipients:
                    try:
                        # Create message for this recipient
                        msg = MIMEMultipart('alternative')
                        msg['From'] = f"Swavlamban 2025 <{self.sender_email}>"
                        msg['To'] = email
                        msg['Subject'] = subject

                        # Add text and HTML parts
                        if text_content:
                            part1 = MIMEText(text_content, 'plain')
                            msg.attach(part1)

                        part2 = MIMEText(html_content, 'html')
                        msg.attach(part2)

                        # Add attachments
                        if attachments:
                            for file_path in attachments:
                                if Path(file_path).exists():
                                    with open(file_path, 'rb') as f:
                                        part = MIMEBase('application', 'octet-stream')
                                        part.set_payload(f.read())
                                        encoders.encode_base64(part)
                                        part.add_header(
                                            'Content-Disposition',
                                            f'attachment; filename={Path(file_path).name}'
                                        )
                                        msg.attach(part)

                        # Send using persistent connection
                        server.send_message(msg)
                        results["success"] += 1
                        print(f"✅ Sent to {email}")

                    except Exception as e:
                        results["failed"] += 1
                        print(f"❌ Failed to send to {email}: {e}")

        except Exception as e:
            print(f"❌ Bulk email connection failed: {e}")
            results["failed"] = len(recipients) - results["success"]

        return results

    def send_pass_email(self, to_email: str, name: str, pass_files: List[str],
                       pass_type: str = "exhibition_day1") -> bool:
        """
        Send event pass email with QR code attachments

        Args:
            to_email: Recipient email
            name: Recipient name
            pass_files: List of pass file paths
            pass_type: Type of pass

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Email templates
            templates = {
                "exhibition_day1": {
                    "subject": "Swavlamban 2025 - Exhibition Pass (Day 1 - 25 November)",
                    "html": f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1D4E89;">Swavlamban 2025 - Exhibition Pass</h2>
        <p>Dear {name},</p>
        <p>Your exhibition pass for <strong>Swavlamban 2025 - Day 1</strong> has been generated.</p>
        <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #1D4E89;">EVENT DETAILS:</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li>📅 <strong>Date:</strong> 25 November 2025 (Monday)</li>
                <li>🕐 <strong>Time:</strong> 1100 - 1730 hrs</li>
                <li>📍 <strong>Venue:</strong> Exhibition Hall</li>
            </ul>
        </div>
        <p><strong>Please find your pass attached.</strong> Print or show on your mobile at the entry gate.</p>
        <p style="margin-top: 30px;">For support: <a href="mailto:niio-tdac@navy.gov.in">niio-tdac@navy.gov.in</a></p>
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 14px;">
                Best regards,<br><strong>Team Swavlamban 2025</strong><br>Indian Navy | Innovation & Self-Reliance
            </p>
        </div>
    </div>
</body>
</html>"""
                },
                "exhibition_day2": {
                    "subject": "Swavlamban 2025 - Exhibition Pass (Day 2 - 26 November)",
                    "html": f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1D4E89;">Swavlamban 2025 - Exhibition Pass</h2>
        <p>Dear {name},</p>
        <p>Your exhibition pass for <strong>Swavlamban 2025 - Day 2</strong> has been generated.</p>
        <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #1D4E89;">EVENT DETAILS:</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li>📅 <strong>Date:</strong> 26 November 2025 (Tuesday)</li>
                <li>🕐 <strong>Time:</strong> 1000 - 1730 hrs</li>
                <li>📍 <strong>Venue:</strong> Exhibition Hall</li>
            </ul>
        </div>
        <p><strong>Please find your pass attached.</strong></p>
        <p>For support: <a href="mailto:niio-tdac@navy.gov.in">niio-tdac@navy.gov.in</a></p>
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 14px;">
                Best regards,<br><strong>Team Swavlamban 2025</strong><br>Indian Navy
            </p>
        </div>
    </div>
</body>
</html>"""
                }
            }

            template = templates.get(pass_type, templates["exhibition_day1"])

            return self.send_email(
                to_email=to_email,
                subject=template["subject"],
                html_content=template["html"],
                attachments=pass_files
            )

        except Exception as e:
            print(f"Error sending pass email: {e}")
            return False
