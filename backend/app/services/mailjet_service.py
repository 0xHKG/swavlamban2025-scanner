"""
Mailjet API Service
Fast email sending using Mailjet REST API v3.1
Much faster than SMTP (10s vs 90s per email)
Uses official mailjet-rest library (proven to work in 2024)
"""
from mailjet_rest import Client
import base64
import time
from pathlib import Path
from typing import List, Optional

from ..core.config import settings


class MailjetService:
    """Service for sending emails via Mailjet API v3.1"""

    def __init__(self):
        """Initialize Mailjet API service using official mailjet-rest library"""
        self.api_key = settings.MAILJET_API_KEY
        self.api_secret = settings.MAILJET_API_SECRET
        self.sender_email = settings.GMAIL_ADDRESS  # Use Gmail as sender (validated in Mailjet)
        self.sender_name = "Swavlamban 2025"

    def send_email(self, to_email: str, subject: str, html_content: str,
                   text_content: str = "", attachments: List[str] = None) -> bool:
        """
        Send email via Mailjet API v3.1 using official mailjet-rest library

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

            # Initialize Mailjet client (2024 pattern - PROVEN TO WORK)
            mailjet = Client(
                auth=(self.api_key, self.api_secret),
                version='v3.1'
            )

            # Build message payload
            message = {
                "From": {
                    "Email": self.sender_email,
                    "Name": self.sender_name
                },
                "To": [
                    {
                        "Email": to_email
                    }
                ],
                "Subject": subject,
                "HTMLPart": html_content
            }

            # Add text part if provided
            if text_content:
                message["TextPart"] = text_content

            # Add attachments
            attachment_start = time.time()
            if attachments:
                message["Attachments"] = []
                for file_path in attachments:
                    if Path(file_path).exists():
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                            file_name = Path(file_path).name

                            # Determine content type based on extension
                            if file_name.endswith('.png'):
                                content_type = "image/png"
                            elif file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
                                content_type = "image/jpeg"
                            elif file_name.endswith('.pdf'):
                                content_type = "application/pdf"
                            else:
                                content_type = "application/octet-stream"

                            message["Attachments"].append({
                                "ContentType": content_type,
                                "Filename": file_name,
                                "Base64Content": base64.b64encode(file_data).decode('utf-8')
                            })
            attachment_time = time.time() - attachment_start

            # Build full payload
            data = {
                "Messages": [message]
            }

            # Send via Mailjet official library (2024 pattern - PROVEN TO WORK)
            api_start = time.time()
            print(f"📤 Sending to Mailjet API (official library): {to_email}")
            print(f"   API Key: {self.api_key[:10]}...")

            result = mailjet.send.create(data=data)
            api_time = time.time() - api_start

            total_time = time.time() - start_time

            print(f"📬 Mailjet API Response: Status={result.status_code}, Time={api_time:.1f}s")
            if result.status_code != 200:
                print(f"   Response body: {result.json()}")

            # Check response
            if result.status_code == 200:
                response_data = result.json()
                if response_data.get("Messages") and len(response_data["Messages"]) > 0:
                    msg_status = response_data["Messages"][0].get("Status")
                    if msg_status == "success":
                        print(f"✅ Email sent successfully to {to_email} via Mailjet API")
                        print(f"   ⏱️ Timing breakdown: Total={total_time:.1f}s | Attachments={attachment_time:.1f}s | API={api_time:.1f}s")
                        return True
                    else:
                        errors = response_data["Messages"][0].get("Errors", [])
                        print(f"❌ Mailjet API returned error status for {to_email}")
                        for error in errors:
                            print(f"   Error: {error.get('ErrorMessage', 'Unknown error')}")
                        return False
            else:
                print(f"❌ Mailjet API request failed with status {result.status_code}")
                print(f"   Response: {result.json()}")
                return False

        except Exception as e:
            print(f"❌ Failed to send email to {to_email} via Mailjet API: {e}")
            return False

    def send_bulk_email(self, recipients: List[dict], subject: str,
                       html_content: str, text_content: str = "",
                       attachments: List[str] = None) -> dict:
        """
        Send bulk emails via Mailjet API v3.1 using official mailjet-rest library

        Args:
            recipients: List of dicts with 'email' and 'name' keys
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)
            attachments: List of file paths to attach

        Returns:
            dict: Results with success_count, failed_count, and errors
        """
        try:
            start_time = time.time()

            # Initialize Mailjet client (2024 pattern - PROVEN TO WORK)
            mailjet = Client(
                auth=(self.api_key, self.api_secret),
                version='v3.1'
            )

            # Build messages array (one message per recipient for proper tracking)
            messages = []

            # Prepare attachments once (reused for all messages)
            attachment_list = []
            if attachments:
                for file_path in attachments:
                    if Path(file_path).exists():
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                            file_name = Path(file_path).name

                            # Determine content type
                            if file_name.endswith('.png'):
                                content_type = "image/png"
                            elif file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
                                content_type = "image/jpeg"
                            elif file_name.endswith('.pdf'):
                                content_type = "application/pdf"
                            else:
                                content_type = "application/octet-stream"

                            attachment_list.append({
                                "ContentType": content_type,
                                "Filename": file_name,
                                "Base64Content": base64.b64encode(file_data).decode('utf-8')
                            })

            # Create message for each recipient
            for recipient in recipients:
                message = {
                    "From": {
                        "Email": self.sender_email,
                        "Name": self.sender_name
                    },
                    "To": [
                        {
                            "Email": recipient['email'],
                            "Name": recipient.get('name', '')
                        }
                    ],
                    "Subject": subject,
                    "HTMLPart": html_content
                }

                if text_content:
                    message["TextPart"] = text_content

                if attachment_list:
                    message["Attachments"] = attachment_list

                messages.append(message)

            # Build payload
            data = {
                "Messages": messages
            }

            # Send via Mailjet official library (2024 pattern - PROVEN TO WORK)
            result = mailjet.send.create(data=data)

            total_time = time.time() - start_time

            # Process response
            results = {
                'success_count': 0,
                'failed_count': 0,
                'errors': []
            }

            if result.status_code == 200:
                response_data = result.json()
                for idx, msg_result in enumerate(response_data.get("Messages", [])):
                    if msg_result.get("Status") == "success":
                        results['success_count'] += 1
                    else:
                        results['failed_count'] += 1
                        recipient_email = recipients[idx]['email']
                        errors = msg_result.get("Errors", [])
                        error_msgs = [e.get('ErrorMessage', 'Unknown error') for e in errors]
                        results['errors'].append({
                            'email': recipient_email,
                            'errors': error_msgs
                        })

                print(f"✅ Bulk email completed: {results['success_count']} success, {results['failed_count']} failed (took {total_time:.1f}s)")
            else:
                print(f"❌ Mailjet bulk API request failed with status {result.status_code}")
                results['failed_count'] = len(recipients)
                results['errors'].append({
                    'error': f"API request failed: {result.json()}"
                })

            return results

        except Exception as e:
            print(f"❌ Failed to send bulk emails via Mailjet API: {e}")
            return {
                'success_count': 0,
                'failed_count': len(recipients) if recipients else 0,
                'errors': [{'error': str(e)}]
            }
