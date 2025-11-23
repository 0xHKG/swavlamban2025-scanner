"""
Email service - Auto-detects and uses configured email provider
Supports: Mailjet API (FAST), NIC SMTP, Gmail SMTP, MailBluster
"""
import base64
from pathlib import Path
from typing import List, Optional

from ..core.config import settings


class EmailService:
    """Unified email service - automatically uses configured provider"""
    
    # Email templates for different pass types
    EMAIL_TEMPLATES = {
        "exhibition_day1": {
            "subject": "Swavlamban 2025 - Exhibition Pass (Day 1 - 25 November)",
            "body": """Dear {name},

Your exhibition pass for Swavlamban 2025 - Day 1 has been generated.

EVENT DETAILS:
- Date: 25 November 2025 (Monday)
- Time: 1100 - 1730 hrs
- Venue: Exhibition Hall, Manekshaw Centre

ACCESS:
• Exhibition viewing
• Industry booths and stalls
• Innovation displays

Please find your pass attached. Print or show this pass on your mobile device at the entry gate.

For support: niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy | Innovation & Self-Reliance"""
        },
        "exhibition_day2": {
            "subject": "Swavlamban 2025 - Exhibition Pass (Day 2 - 26 November)",
            "body": """Dear {name},

Your exhibition pass for Swavlamban 2025 - Day 2 has been generated.

EVENT DETAILS:
- Date: 26 November 2025 (Tuesday)
- Time: 1000 - 1730 hrs
- Venue: Exhibition Hall, Manekshaw Centre

ACCESS:
• Exhibition viewing
• Industry booths and stalls
• Innovation displays

Please find your pass attached. Print or show this pass on your mobile device at the entry gate.

For support: niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy | Innovation & Self-Reliance"""
        },
        "exhibition_both_days_exhibitor": {
            "subject": "Swavlamban 2025 - Exhibitor Passes (25-26 November)",
            "body": """Dear {name},

Your exhibitor passes for Swavlamban 2025 have been generated.

EVENT DETAILS:
- Dates: 25-26 November 2025
- Time: Day 1: 1100-1730 hrs | Day 2: 1000-1730 hrs
- Venue: Exhibition Hall, Manekshaw Centre

STALL SETUP:
• Venue will be available for stall setup on AM 24 Nov 25
• Dimensions of stalls: 3m X 2.5m

EXHIBITOR ACCESS:
• Full access to Exhibition Hall on both days
• Booth setup and operations
• Industry interactions

Please find your passes attached. These passes grant access to both days.

For support: niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy | Innovation & Self-Reliance"""
        },
        "interactive_sessions": {
            "subject": "Swavlamban 2025 - Panel Discussions Pass (26 November)",
            "body": """Dear {name},

Your pass for Panel Discussions at Swavlamban 2025 has been generated.

SESSIONS:
• Panel Discussion I: Future & Emerging Technologies (1030-1130 hrs)
• Panel Discussion II: Boosting iDEX Ecosystem (1200-1330 hrs)

EVENT DETAILS:
- Date: 26 November 2025 (Tuesday)
- Venue: Zorawar Hall, Manekshaw Centre

IMPORTANT:
• Please arrive by 1020 hrs for Panel I
• Seating is limited
• Late entry may not be permitted

Please find your pass attached. Print or show this pass on your mobile device at the entry gate.

For support: niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy | Innovation & Self-Reliance"""
        },
        "plenary": {
            "subject": "Swavlamban 2025 - Plenary Session Pass (26 November)",
            "body": """Dear {name},

Your pass for the Plenary Session at Swavlamban 2025 has been generated.

SESSION DETAILS:
- Date: 26 November 2025 (Tuesday)
- Time: 1530 - 1615 hrs
- Venue: Zorawar Hall, Manekshaw Centre

HIGHLIGHTS:
• Address by Chief Guest
• CNS Welcome Address
• Release of Books/Documents/MoUs
• Discussions on 'Innovation & Self-reliance'

SPECIAL NOTES:
• Please be seated by 1620 hrs
• Formal dress code mandatory
• Security clearance required

Please find your pass attached. Print or show this pass on your mobile device at the entry gate.

For support: niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy | Innovation & Self-Reliance"""
        }
    }
    
    def __init__(self):
        """Initialize email service based on configuration"""
        self.provider = None
        self._initialized = False

    def _ensure_provider_initialized(self):
        """Lazy initialization - called when email service is first used"""
        if self._initialized:
            return

        print("🔄 Initializing email provider...")

        # Determine which email provider to use (Priority order)
        # 1. Brevo API (PRIMARY - formerly Sendinblue) ⚡
        if settings.USE_BREVO and settings.BREVO_API_KEY:
            from .brevo_service import BrevoService
            self.provider = BrevoService()
            self.provider_name = "Brevo API"
            self.uses_smtp = True  # Treats file paths like SMTP (not base64 encoding)
            print("✅ Using Brevo API (PRIMARY - fast transactional email)")
        # 2. Mailjet API (STANDBY - fallback if Brevo fails) ⚡
        elif settings.MAILJET_API_KEY and settings.MAILJET_API_SECRET:
            from .mailjet_service import MailjetService
            self.provider = MailjetService()
            self.provider_name = "Mailjet API"
            self.uses_smtp = True  # Treats file paths like SMTP (not base64 encoding)
            print("✅ Using Mailjet API (STANDBY - ~10s per email)")
        # 3. Gmail SMTP (Final fallback - personal email)
        elif settings.USE_GMAIL_SMTP and settings.GMAIL_ADDRESS:
            from .gmail_smtp_service import GmailSMTPService
            self.provider = GmailSMTPService()
            self.provider_name = "Gmail SMTP"
            self.uses_smtp = True
            print(f"✅ Using Gmail SMTP: {settings.GMAIL_ADDRESS} (Final fallback)")
        # 4. NIC SMTP (Government email - Official Navy correspondence - SLOW)
        elif settings.USE_NIC_SMTP and settings.NIC_EMAIL_ADDRESS:
            from .nic_smtp_service import NICSmtpService
            self.provider = NICSmtpService()
            self.provider_name = "NIC SMTP (Navy Email)"
            self.uses_smtp = True
            print(f"✅ Using NIC SMTP: {settings.NIC_EMAIL_ADDRESS} (SLOW - ~90s per email)")
        # 4. MailBluster (API-based)
        elif settings.MAILBLUSTER_API_KEY:
            from .mailbluster_service import MailBlusterService
            self.provider = MailBlusterService()
            self.provider_name = "MailBluster"
            self.uses_smtp = False
            print("✅ Using MailBluster API")
        # Fallback
        else:
            print("⚠️ Warning: No email service configured!")
            self.provider_name = "None"
            self.uses_smtp = False

        self._initialized = True
    
    def send_pass_email(self, recipient_email: str, recipient_name: str,
                       pass_files: List[Path], pass_type: str = None) -> bool:
        """Send pass email with attachments using configured provider"""

        # Ensure provider is initialized (lazy initialization after secrets are loaded)
        self._ensure_provider_initialized()

        # Detect which passes are being sent from filenames
        pass_types_detected = []
        has_invitations = False

        for pass_file in pass_files:
            filename = pass_file.name.lower()

            # Check for invitation images
            if "inv-" in filename or "invitation" in filename:
                has_invitations = True

            # Check for QR code passes ONLY (exclude invitation images)
            # Pass files are named: name_id_passtype.png (e.g., abhishek_1_exhibition_day1_visitor.png)
            # Invitation files start with "Inv-" and should NOT be counted as passes

            # Skip invitation files from pass type detection
            if filename.startswith("Inv-") or filename.startswith("inv-"):
                continue

            if "exhibition_day1" in filename or "ep-25" in filename:
                if "exhibition_day1" not in pass_types_detected:
                    pass_types_detected.append("exhibition_day1")
            elif "exhibition_day2" in filename or "ep-26" in filename:
                if "exhibition_day2" not in pass_types_detected:
                    pass_types_detected.append("exhibition_day2")
            elif "interactive" in filename:
                if "interactive_sessions" not in pass_types_detected:
                    pass_types_detected.append("interactive_sessions")
            elif "plenary" in filename:
                if "plenary" not in pass_types_detected:
                    pass_types_detected.append("plenary")

        # Build comprehensive email based on ALL passes being sent
        # Determine singular/plural for better UX
        pass_count = len(pass_types_detected)
        pass_word = "pass" if pass_count == 1 else "passes"
        subject = f"Swavlamban 2025 - Your Event {pass_word.title()}"

        # Build pass details section with line gaps
        pass_details = []

        if "exhibition_day1" in pass_types_detected:
            pass_details.append("""📅 EXHIBITION DAY 1 (25 November 2025)
- Time: 1100 - 1730 hrs
- Venue: Exhibition Hall, Manekshaw Centre
- Access: Exhibition viewing, Industry booths
""")

        if "exhibition_day2" in pass_types_detected:
            pass_details.append("""📅 EXHIBITION DAY 2 (26 November 2025)
- Time: 1000 - 1730 hrs
- Venue: Exhibition Hall, Manekshaw Centre
- Access: Exhibition viewing, Industry booths
""")

        if "interactive_sessions" in pass_types_detected:
            pass_details.append("""💡 INTERACTIVE SESSIONS (26 November 2025)
- Session I: Future & Emerging Technologies (1030-1130 hrs)
- Session II: Boosting iDEX Ecosystem (1200-1330 hrs)
- Venue: Zorawar Hall, Manekshaw Centre
""")

        if "plenary" in pass_types_detected:
            pass_details.append("""🎤 PLENARY SESSION (26 November 2025)
- Time: 1530 - 1615 hrs
- Venue: Zorawar Hall, Manekshaw Centre
- Highlights: Chief Guest Address, Book/MoU Releases
""")

        # Check if user has Interactive or Plenary but NOT Exhibition Day 2
        # Add special note about Exhibition Day 2 access
        has_interactive_or_plenary = ("interactive_sessions" in pass_types_detected or
                                      "plenary" in pass_types_detected)
        has_exhibition_day2 = "exhibition_day2" in pass_types_detected

        exhibition_day2_bonus_note = ""
        if has_interactive_or_plenary and not has_exhibition_day2:
            exhibition_day2_bonus_note = """
📝 BONUS ACCESS - EXHIBITION DAY 2:
Your Interactive/Plenary pass also grants you access to the Exhibition Hall on 26 November 2025 (1000-1730 hrs). Feel free to explore the industry booths and innovation displays!

"""

        # Create comprehensive email body
        # Capitalize first letter of each word in name (Title Case)
        formatted_name = recipient_name.title()

        body = f"""Dear {formatted_name},

Your {pass_word} for Swavlamban 2025 {'has' if pass_count == 1 else 'have'} been generated successfully!

{'='*60}
YOUR {'PASS' if pass_count == 1 else 'PASSES'}:
{'='*60}

{chr(10).join(pass_details)}
{exhibition_day2_bonus_note}{'='*60}
ATTACHMENTS:
{'='*60}

✅ Event {pass_word.title()} with QR Code (for entry gate scanning){f"{chr(10)}✅ Invitation Images" if has_invitations else ""}

{'='*60}
IMPORTANT INFORMATION:
{'='*60}

• PRINT or SHOW the QR code {pass_word} at entry gates
• Arrive 15 minutes before session start time
• Valid photo ID required for entry
• Security clearance mandatory for all sessions

📍 VENUE LOCATION & NAVIGATION:
Manekshaw Centre
Address: H4QW+2MW, Khyber Lines, Delhi Cantonment, New Delhi, Delhi 110010
🗺️ Open in Google Maps: https://www.google.com/maps/dir/?api=1&destination=28.586103304500742,77.14529897550334

📲 EVENT INFORMATION PAGE:
For complete event details, visit our dedicated information page:
https://swavlamban2025-info.streamlit.app/

Available information:
• Venue map & directions (with GPS navigation)
• Complete event schedule
• Guidelines (DOs & DON'Ts)
• FAQs & important contacts

For support or queries, contact:
📞 011-26771528
📧 niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy | Innovation & Self-Reliance"""

        html_body = body.replace('\n', '<br>')

        print(f"📧 Sending email via {self.provider_name}...")
        print(f"   Passes detected: {', '.join(pass_types_detected)}")
        print(f"   Total attachments: {len(pass_files)} (QR passes only)")

        # Use configured email provider
        if self.provider:
            try:
                # SMTP providers (NIC SMTP, Gmail SMTP) use file paths directly
                if self.uses_smtp:
                    success = self.provider.send_email(
                        to_email=recipient_email,
                        subject=subject,
                        html_content=html_body,
                        text_content=body,
                        attachments=pass_files  # Pass file paths directly
                    )
                else:
                    # API-based providers (MailBluster) use base64 encoded attachments
                    attachments = []
                    for pass_file in pass_files:
                        if not pass_file.exists():
                            print(f"Warning: Pass file not found: {pass_file}")
                            continue

                        with open(pass_file, "rb") as f:
                            file_data = base64.b64encode(f.read()).decode()

                        attachments.append({
                            "filename": pass_file.name,
                            "content": file_data,
                            "type": "image/png"
                        })

                    success = self.provider.send_transactional_email(
                        to_email=recipient_email,
                        subject=subject,
                        html_content=html_body,
                        text_content=body,
                        attachments=attachments,
                        from_name="Swavlamban 2025 Team"
                    )

                if success:
                    print(f"✅ Email sent successfully to {recipient_email} via {self.provider_name}")
                else:
                    print(f"❌ Email failed via {self.provider_name}")
                return success

            except Exception as e:
                print(f"❌ Email error ({self.provider_name}): {e}")
                return False

        # Fallback to Mailjet (legacy)
        else:
            # Prepare attachments for Mailjet
            attachments = []
            for pass_file in pass_files:
                if not pass_file.exists():
                    print(f"Warning: Pass file not found: {pass_file}")
                    continue

                with open(pass_file, "rb") as f:
                    file_data = base64.b64encode(f.read()).decode()

                attachments.append({
                    "ContentType": "image/png",
                    "Filename": pass_file.name,
                    "Base64Content": file_data
                })

            # Prepare email data
            data = {
                'Messages': [{
                    "From": {
                        "Email": settings.EMAIL_SENDER,
                        "Name": "Swavlamban 2025 Team"
                    },
                    "To": [{
                        "Email": recipient_email,
                        "Name": recipient_name
                    }],
                    "Subject": subject,
                    "TextPart": body,
                    "HTMLPart": html_body,
                    "Attachments": attachments
                }]
            }

            try:
                result = self.mailjet.send.create(data=data)
                if result.status_code == 200:
                    print(f"✅ Email sent successfully to {recipient_email} via Mailjet")
                    return True
                else:
                    print(f"❌ Email failed: {result.status_code} - {result.json()}")
                    return False
            except Exception as e:
                print(f"❌ Email error (Mailjet): {e}")
                return False

    def send_exhibitor_bulk_email(self, recipient_email: str, recipient_name: str,
                                   pass_files: List[Path]) -> bool:
        """
        Send exhibitor passes email - specifically for bulk exhibitor upload
        This is a dedicated function for exhibitors to avoid modifying visitor email logic

        Expected attachments:
        - Multiple QR passes (EP-25n26.png template with unique QR codes, one per attendee)
        - 1 Exhibitor invitation card (Inv-Exhibitors.png)
        """
        # Ensure provider is initialized
        self._ensure_provider_initialized()

        # Count QR passes and check for invitation
        qr_passes = []
        has_invitation = False

        for pass_file in pass_files:
            filename = pass_file.name.lower()
            if filename.startswith("inv-") or "invitation" in filename:
                has_invitation = True
            else:
                qr_passes.append(pass_file.name)

        num_attendees = len(qr_passes)
        pass_word = "pass" if num_attendees == 1 else "passes"

        # Format name to Title Case
        formatted_name = recipient_name.title()

        # Create exhibitor-specific email
        subject = f"Swavlamban 2025 - Exhibitor {pass_word.title()} (25-26 November)"

        body = f"""Dear {formatted_name},

Your exhibitor {pass_word} for Swavlamban 2025 {'has' if num_attendees == 1 else 'have'} been generated.

{'='*60}
EVENT DETAILS:
{'='*60}

• Dates: 25-26 November 2025
• Time: Day 1: 0930-1730 hrs | Day 2: 1000-1730 hrs
• Venue: Exhibition Hall, Manekshaw Centre
• Note: Please arrive by 0930 hrs on Day 1 for inauguration at 1000 hrs

{'='*60}
STALL SETUP:
{'='*60}

• Venue will be available for stall setup on AM 24 Nov 25
• Dimensions of stalls: 3m X 2.5m

{'='*60}
EXHIBITOR ACCESS:
{'='*60}

• Full access to Exhibition Hall on both days
• Booth setup and operations
• Industry interactions

{'='*60}
ATTACHMENTS:
{'='*60}

✅ Event {pass_word.title()} with QR Code (for entry gate scanning){f"{chr(10)}✅ Invitation Card" if has_invitation else ""}

{'='*60}
IMPORTANT INFORMATION:
{'='*60}

• PRINT or SHOW the QR code {pass_word} at entry gates
• Valid Aadhar Card required for entry
• Security clearance mandatory for all attendees

📍 VENUE LOCATION & NAVIGATION:
Manekshaw Centre
Address: H4QW+2MW, Khyber Lines, Delhi Cantonment, New Delhi, Delhi 110010
🗺️ Open in Google Maps: https://www.google.com/maps/dir/?api=1&destination=28.586103304500742,77.14529897550334

📲 EVENT INFORMATION:
For complete event details, visit https://swavlamban2025-info.streamlit.app

For support or queries, contact:
📞 011-26771528
📧 niio-tdac@navy.gov.in

Best regards,
Team Swavlamban 2025
Indian Navy | Innovation & Self-Reliance"""

        html_body = body.replace('\n', '<br>')

        print(f"📧 Sending exhibitor email via {self.provider_name}...")
        print(f"   Exhibitor: {recipient_name}")
        print(f"   Attendees: {num_attendees}")
        print(f"   Total attachments: {len(pass_files)}")

        # Use configured email provider
        if self.provider:
            try:
                # SMTP providers (NIC SMTP, Gmail SMTP) use file paths directly
                if self.uses_smtp:
                    success = self.provider.send_email(
                        to_email=recipient_email,
                        subject=subject,
                        html_content=html_body,
                        text_content=body,
                        attachments=pass_files
                    )
                else:
                    # API-based providers (MailBluster) use base64 encoded attachments
                    attachments = []
                    for pass_file in pass_files:
                        if not pass_file.exists():
                            print(f"Warning: Pass file not found: {pass_file}")
                            continue

                        with open(pass_file, "rb") as f:
                            file_data = base64.b64encode(f.read()).decode()

                        attachments.append({
                            "filename": pass_file.name,
                            "content": file_data,
                            "type": "image/png"
                        })

                    success = self.provider.send_transactional_email(
                        to_email=recipient_email,
                        subject=subject,
                        html_content=html_body,
                        text_content=body,
                        attachments=attachments,
                        from_name="Swavlamban 2025 Team"
                    )

                if success:
                    print(f"✅ Exhibitor email sent successfully to {recipient_email}")
                else:
                    print(f"❌ Exhibitor email failed")
                return success

            except Exception as e:
                print(f"❌ Exhibitor email error: {e}")
                return False

        # Fallback to Mailjet (legacy)
        else:
            attachments = []
            for pass_file in pass_files:
                if not pass_file.exists():
                    print(f"Warning: Pass file not found: {pass_file}")
                    continue

                with open(pass_file, "rb") as f:
                    file_data = base64.b64encode(f.read()).decode()

                attachments.append({
                    "ContentType": "image/png",
                    "Filename": pass_file.name,
                    "Base64Content": file_data
                })

            data = {
                'Messages': [{
                    "From": {
                        "Email": settings.EMAIL_SENDER,
                        "Name": "Swavlamban 2025 Team"
                    },
                    "To": [{
                        "Email": recipient_email,
                        "Name": recipient_name
                    }],
                    "Subject": subject,
                    "TextPart": body,
                    "HTMLPart": html_body,
                    "Attachments": attachments
                }]
            }

            try:
                result = self.mailjet.send.create(data=data)
                if result.status_code == 200:
                    print(f"✅ Exhibitor email sent to {recipient_email} via Mailjet")
                    return True
                else:
                    print(f"❌ Exhibitor email failed: {result.status_code}")
                    return False
            except Exception as e:
                print(f"❌ Exhibitor email error (Mailjet): {e}")
                return False


# Create singleton instance
email_service = EmailService()
