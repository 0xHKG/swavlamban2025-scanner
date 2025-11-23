"""
Brevo API Service (formerly Sendinblue)
Fast transactional email sending using Brevo REST API v3
Uses official sib-api-v3-sdk library
"""
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import base64
import time
from pathlib import Path
from typing import List, Optional

from ..core.config import settings


class BrevoService:
    """Service for sending emails via Brevo API v3"""

    def __init__(self):
        """Initialize Brevo API service using official sib-api-v3-sdk library"""
        self.api_key = settings.BREVO_API_KEY
        self.sender_email = settings.GMAIL_ADDRESS  # swavlamban2025@gmail.com
        self.sender_name = "Swavlamban 2025"

        # Configure API client
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = self.api_key

        # Initialize API instance
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(self.configuration)
        )

    def send_email(self, to_email: str, subject: str, html_content: str,
                   text_content: str = "", attachments: List[str] = None) -> bool:
        """
        Send email via Brevo API v3

        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional, not used by Brevo)
            attachments: List of file paths to attach

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            start_time = time.time()

            # Prepare sender
            sender = {
                "name": self.sender_name,
                "email": self.sender_email
            }

            # Prepare recipient
            to = [{"email": to_email}]

            # Prepare attachments
            attachment_start = time.time()
            brevo_attachments = []

            if attachments:
                for file_path in attachments:
                    if Path(file_path).exists():
                        try:
                            # Read and encode file to base64
                            with open(file_path, 'rb') as f:
                                file_data = f.read()
                                encoded_string = base64.b64encode(file_data)
                                base64_content = encoded_string.decode('utf-8')

                            file_name = Path(file_path).name

                            # Add to attachments list
                            brevo_attachments.append({
                                "content": base64_content,
                                "name": file_name
                            })

                        except Exception as e:
                            print(f"⚠️  Failed to attach {file_path}: {e}")
                            continue

            attachment_time = time.time() - attachment_start

            # Create email object
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=to,
                sender=sender,
                subject=subject,
                html_content=html_content,
                attachment=brevo_attachments if brevo_attachments else None
            )

            # Send email
            send_start = time.time()
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            send_time = time.time() - send_start

            total_time = time.time() - start_time

            print(f"✅ Brevo email sent successfully to {to_email}")
            print(f"   Message ID: {api_response.message_id if hasattr(api_response, 'message_id') else 'N/A'}")
            print(f"   Total: {total_time:.1f}s | Attachments: {attachment_time:.1f}s | Send: {send_time:.1f}s")

            return True

        except ApiException as e:
            print(f"❌ Brevo API error: {e}")
            print(f"   Status: {e.status if hasattr(e, 'status') else 'Unknown'}")
            print(f"   Reason: {e.reason if hasattr(e, 'reason') else 'Unknown'}")
            print(f"   Body: {e.body if hasattr(e, 'body') else 'No details'}")
            return False

        except Exception as e:
            print(f"❌ Unexpected error sending email via Brevo: {e}")
            import traceback
            traceback.print_exc()
            return False


# Example usage and testing
if __name__ == "__main__":
    """Test Brevo service directly"""
    print("🧪 Testing Brevo Email Service")
    print("=" * 50)

    # Initialize service
    service = BrevoService()

    # Test email
    test_email = "abhishekvardhan86@gmail.com"
    test_subject = "Swavlamban 2025 - Brevo Test Email"
    test_html = """
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #003366;">Swavlamban 2025</h2>
        <p>This is a test email from the Brevo API integration.</p>
        <p><strong>Email Provider:</strong> Brevo (formerly Sendinblue)</p>
        <p><strong>Sender:</strong> swavlamban2025@gmail.com</p>
        <hr>
        <p style="color: #666; font-size: 12px;">
            Indian Navy | Innovation & Self-Reliance
        </p>
    </body>
    </html>
    """

    # Test without attachments
    print("\n📧 Test 1: Simple email (no attachments)")
    success = service.send_email(
        to_email=test_email,
        subject=test_subject,
        html_content=test_html
    )

    if success:
        print("✅ Test 1 passed!")
    else:
        print("❌ Test 1 failed!")

    # Test with attachments (if available)
    print("\n📧 Test 2: Email with attachments")
    test_file = Path("test_attachment.txt")

    # Create a test file
    if not test_file.exists():
        test_file.write_text("This is a test attachment for Brevo integration.")

    if test_file.exists():
        success = service.send_email(
            to_email=test_email,
            subject=f"{test_subject} (With Attachment)",
            html_content=test_html,
            attachments=[str(test_file)]
        )

        if success:
            print("✅ Test 2 passed!")
        else:
            print("❌ Test 2 failed!")

        # Cleanup test file
        test_file.unlink()
    else:
        print("⚠️  Test 2 skipped (no test file)")

    print("\n" + "=" * 50)
    print("🎉 Brevo service testing complete!")
