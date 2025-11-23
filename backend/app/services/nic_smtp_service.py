"""
NIC SMTP Integration Service
Free email sending using NIC SMTP for Government email addresses (navy.gov.in)
Server: smtp.mgovcloud.in
"""
import smtplib
import base64
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional

from ..core.config import settings


class NICSmtpService:
    """Service for sending emails via NIC SMTP (Government Email)"""

    def __init__(self):
        """Initialize NIC SMTP service"""
        self.smtp_server = "smtp.mgovcloud.in"
        self.smtp_port = 465  # SSL (changed from 587 TLS to test)
        self.sender_email = settings.NIC_EMAIL_ADDRESS
        self.sender_password = settings.NIC_EMAIL_PASSWORD
        self.use_ssl = True  # Use SSL (port 465) instead of TLS

    def send_email(self, to_email: str, subject: str, html_content: str,
                   text_content: str = "", attachments: List[str] = None) -> bool:
        """
        Send email via NIC SMTP

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
            start_time = time.time()

            # Create message
            msg_start = time.time()
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
            attachment_start = time.time()
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
            attachment_time = time.time() - attachment_start

            # Send email using SSL (port 465) instead of TLS (port 587)
            # Use SMTP_SSL for port 465 instead of SMTP with STARTTLS
            smtp_start = time.time()
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=30) as server:
                # Disable debug mode for faster sending (was causing 30-60s delays)
                # server.set_debuglevel(1)  # Commented out for production speed
                login_start = time.time()
                server.login(self.sender_email, self.sender_password)
                login_time = time.time() - login_start

                send_start = time.time()
                server.send_message(msg)
                send_time = time.time() - send_start

            smtp_time = time.time() - smtp_start
            total_time = time.time() - start_time

            print(f"✅ Email sent successfully to {to_email} via NIC SMTP")
            print(f"   ⏱️ Timing breakdown: Total={total_time:.1f}s | Attachments={attachment_time:.1f}s | SMTP={smtp_time:.1f}s (Login={login_time:.1f}s, Send={send_time:.1f}s)")
            return True

        except Exception as e:
            print(f"❌ Failed to send email to {to_email} via NIC SMTP: {e}")
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
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                print(f"✅ Connected to NIC SMTP for bulk sending ({len(recipients)} emails)")

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

    def test_connection(self) -> bool:
        """
        Test SMTP connection and authentication

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                print(f"✅ NIC SMTP connection test successful!")
                print(f"   Server: {self.smtp_server}:{self.smtp_port}")
                print(f"   Email: {self.sender_email}")
                return True
        except Exception as e:
            print(f"❌ NIC SMTP connection test failed: {e}")
            return False
