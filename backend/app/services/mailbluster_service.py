"""
MailBluster API Integration Service
Handles email sending via MailBluster API
"""
import requests
import base64
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

from ..core.config import settings


class MailBlusterService:
    """Service for sending emails with MailBluster API"""

    API_BASE_URL = "https://api.mailbluster.com/api"

    def __init__(self):
        """Initialize MailBluster service"""
        self.api_key = settings.MAILBLUSTER_API_KEY
        self.brand_id = settings.MAILBLUSTER_BRAND_ID if hasattr(settings, 'MAILBLUSTER_BRAND_ID') else None

    def _get_headers(self) -> Dict[str, str]:
        """Get API headers with authorization"""
        return {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }

    def create_or_update_lead(self, email: str, first_name: str = "", last_name: str = "",
                             subscribed: bool = True, tags: List[str] = None) -> bool:
        """
        Create or update a lead in MailBluster

        Args:
            email: Email address
            first_name: First name
            last_name: Last name
            subscribed: Whether lead is subscribed
            tags: List of tags to assign

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = f"{self.API_BASE_URL}/leads"

            payload = {
                "email": email,
                "subscribed": subscribed
            }

            if first_name:
                payload["firstName"] = first_name
            if last_name:
                payload["lastName"] = last_name
            if tags:
                payload["tags"] = tags

            response = requests.post(url, json=payload, headers=self._get_headers())

            if response.status_code in [200, 201]:
                return True
            else:
                print(f"MailBluster API error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error creating lead: {e}")
            return False

    def send_transactional_email(self, to_email: str, subject: str, html_content: str,
                                 text_content: str = "", attachments: List[Dict] = None,
                                 from_email: str = None, from_name: str = None) -> bool:
        """
        Send a transactional email via MailBluster

        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)
            attachments: List of attachments (optional)
            from_email: Sender email (optional, uses default if not provided)
            from_name: Sender name (optional)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = f"{self.API_BASE_URL}/emails/send"

            payload = {
                "to": to_email,
                "subject": subject,
                "html": html_content
            }

            if text_content:
                payload["text"] = text_content

            if from_email:
                payload["from_email"] = from_email
            if from_name:
                payload["from_name"] = from_name

            # Add attachments if provided
            if attachments:
                payload["attachments"] = attachments

            response = requests.post(url, json=payload, headers=self._get_headers())

            if response.status_code in [200, 201]:
                return True
            else:
                print(f"MailBluster send error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_bulk_email(self, recipients: List[str], subject: str, html_content: str,
                       text_content: str = "", from_email: str = None,
                       from_name: str = "Swavlamban 2025") -> Dict[str, int]:
        """
        Send bulk emails to multiple recipients

        Args:
            recipients: List of email addresses
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)
            from_email: Sender email (optional)
            from_name: Sender name (optional)

        Returns:
            dict: {"success": count, "failed": count}
        """
        results = {"success": 0, "failed": 0}

        for email in recipients:
            success = self.send_transactional_email(
                to_email=email,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                from_email=from_email,
                from_name=from_name
            )

            if success:
                results["success"] += 1
            else:
                results["failed"] += 1

        return results

    def send_pass_email(self, to_email: str, name: str, pass_files: List[str],
                       pass_type: str = "exhibition_day1") -> bool:
        """
        Send event pass email with QR code attachments

        Args:
            to_email: Recipient email
            name: Recipient name
            pass_files: List of pass file paths
            pass_type: Type of pass (determines email template)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get email template based on pass type
            templates = {
                "exhibition_day1": {
                    "subject": "Swavlamban 2025 - Exhibition Pass (Day 1 - 25 November)",
                    "body": f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1D4E89;">Swavlamban 2025 - Exhibition Pass</h2>

        <p>Dear {name},</p>

        <p>Your exhibition pass for <strong>Swavlamban 2025 - Day 1</strong> has been generated.</p>

        <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #1D4E89; margin-top: 0;">EVENT DETAILS:</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li>📅 <strong>Date:</strong> 25 November 2025 (Monday)</li>
                <li>🕐 <strong>Time:</strong> 1100 - 1730 hrs</li>
                <li>📍 <strong>Venue:</strong> Exhibition Hall</li>
            </ul>
        </div>

        <div style="background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #1D4E89; margin-top: 0;">ACCESS:</h3>
            <ul>
                <li>Exhibition viewing</li>
                <li>Industry booths and stalls</li>
                <li>Innovation displays</li>
            </ul>
        </div>

        <p><strong>Please find your pass attached.</strong> Print or show this pass on your mobile device at the entry gate.</p>

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
</html>"""
                },
                "exhibition_day2": {
                    "subject": "Swavlamban 2025 - Exhibition Pass (Day 2 - 26 November)",
                    "body": f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1D4E89;">Swavlamban 2025 - Exhibition Pass</h2>

        <p>Dear {name},</p>

        <p>Your exhibition pass for <strong>Swavlamban 2025 - Day 2</strong> has been generated.</p>

        <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #1D4E89; margin-top: 0;">EVENT DETAILS:</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li>📅 <strong>Date:</strong> 26 November 2025 (Tuesday)</li>
                <li>🕐 <strong>Time:</strong> 1000 - 1730 hrs</li>
                <li>📍 <strong>Venue:</strong> Exhibition Hall</li>
            </ul>
        </div>

        <p><strong>Please find your pass attached.</strong> Print or show this pass on your mobile device at the entry gate.</p>

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
</html>"""
                },
                "interactive_sessions": {
                    "subject": "Swavlamban 2025 - Panel Discussion Pass (26 November)",
                    "body": f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1D4E89;">Swavlamban 2025 - Panel Discussion Pass</h2>

        <p>Dear {name},</p>

        <p>Your pass for <strong>Panel Discussions</strong> has been generated.</p>

        <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #1D4E89; margin-top: 0;">SESSION DETAILS:</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li>📅 <strong>Date:</strong> 26 November 2025 (Tuesday)</li>
                <li>📍 <strong>Venue:</strong> Zorawar Hall</li>
            </ul>
        </div>

        <p><strong>Please arrive 15 minutes before your session starts.</strong></p>

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
</html>"""
                },
                "plenary": {
                    "subject": "Swavlamban 2025 - Plenary Session Pass (26 November)",
                    "body": f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1D4E89;">Swavlamban 2025 - Plenary Session Pass</h2>

        <p>Dear {name},</p>

        <p>Your pass for the <strong>Plenary Session</strong> has been generated.</p>

        <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #1D4E89; margin-top: 0;">SESSION DETAILS:</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li>📅 <strong>Date:</strong> 26 November 2025 (Tuesday)</li>
                <li>🕐 <strong>Time:</strong> 1530 - 1615 hrs (Gates open at 1500)</li>
                <li>📍 <strong>Venue:</strong> Zorawar Hall</li>
            </ul>
        </div>

        <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #856404; margin-top: 0;">HIGHLIGHTS:</h3>
            <ul>
                <li>Address by Chief Guest</li>
                <li>CNS Welcome Address</li>
                <li>Release of Books/Documents/MoUs</li>
            </ul>
        </div>

        <p><strong>⚠️ Please be seated by 1620 hrs. Formal dress code mandatory.</strong></p>

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
</html>"""
                }
            }

            template = templates.get(pass_type, templates["exhibition_day1"])

            # Prepare attachments
            attachments = []
            for pass_file in pass_files:
                if Path(pass_file).exists():
                    with open(pass_file, 'rb') as f:
                        file_content = base64.b64encode(f.read()).decode('utf-8')
                        attachments.append({
                            "filename": Path(pass_file).name,
                            "content": file_content,
                            "type": "image/png"
                        })

            # Send email
            return self.send_transactional_email(
                to_email=to_email,
                subject=template["subject"],
                html_content=template["body"],
                attachments=attachments if attachments else None,
                from_name="Swavlamban 2025 Team"
            )

        except Exception as e:
            print(f"Error sending pass email: {e}")
            return False

    def get_lead_info(self, lead_id: str) -> Optional[Dict]:
        """
        Get information about a specific lead

        Args:
            lead_id: Lead ID

        Returns:
            dict: Lead information or None if not found
        """
        try:
            url = f"{self.API_BASE_URL}/leads/{lead_id}"
            response = requests.get(url, headers=self._get_headers())

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except Exception as e:
            print(f"Error getting lead info: {e}")
            return None
