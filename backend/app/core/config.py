"""
Application Configuration
Loads environment variables and provides settings
Supports both .env file (local) and Streamlit secrets (cloud)
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file for local development (will be overridden by secrets if available)
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Swavlamban 2025"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "swavlamban2025"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    # Security
    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production-abc123xyz789"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Email - Brevo (PRIMARY - formerly Sendinblue)
    BREVO_API_KEY: str = ""  # Brevo API key from https://app.brevo.com/settings/keys/api
    USE_BREVO: bool = True  # Set to True to use Brevo as primary email service

    # Email - Mailjet (STANDBY - fallback if Brevo fails)
    MAILJET_API_KEY: str = ""
    MAILJET_API_SECRET: str = ""
    EMAIL_SENDER: str = "noreply@swavlamban2025.in"

    # Email - MailBluster
    MAILBLUSTER_API_KEY: str = ""
    MAILBLUSTER_BRAND_ID: str = ""

    # Email - Gmail SMTP (FREE - Personal)
    GMAIL_ADDRESS: str = ""  # Your Gmail address
    GMAIL_APP_PASSWORD: str = ""  # App-specific password from Google
    USE_GMAIL_SMTP: bool = False  # Set to True to use Gmail SMTP (FREE)

    # Email - NIC SMTP (FREE - Government/Navy Email) - RECOMMENDED
    NIC_EMAIL_ADDRESS: str = ""  # Your NIC email (e.g., niio-tdac@navy.gov.in)
    NIC_EMAIL_PASSWORD: str = ""  # Your NIC email password (or app-specific password)
    USE_NIC_SMTP: bool = True  # Set to True to use NIC SMTP (Government Email)

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8501",
        "http://localhost:3000"
    ]

    # File Upload
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "pdf"]

    # Pass Generation
    PASS_OUTPUT_DIR: str = "../generated_passes"
    IMAGE_ASSETS_DIR: str = "../images"

    # GitHub (Optional)
    GITHUB_PAT: str = ""

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL with URL-encoded password"""
        from urllib.parse import quote_plus
        # URL-encode password to handle special characters like @, :, /, etc.
        encoded_password = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def redis_url(self) -> str:
        """Construct Redis URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    class Config:
        # Look for .env in backend directory
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        case_sensitive = True


# Create settings instance
settings = Settings()

# Override with Streamlit secrets if available (works on both local and cloud)
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        # NIC SMTP settings
        if 'USE_NIC_SMTP' in st.secrets:
            settings.USE_NIC_SMTP = st.secrets.get('USE_NIC_SMTP', False)
            settings.NIC_EMAIL_ADDRESS = st.secrets.get('NIC_EMAIL_ADDRESS', '')
            settings.NIC_EMAIL_PASSWORD = st.secrets.get('NIC_EMAIL_PASSWORD', '')
            print(f"🔑 Loaded NIC SMTP from secrets: {settings.NIC_EMAIL_ADDRESS}")

        # Gmail SMTP settings
        if 'USE_GMAIL_SMTP' in st.secrets:
            settings.USE_GMAIL_SMTP = st.secrets.get('USE_GMAIL_SMTP', False)
            settings.GMAIL_ADDRESS = st.secrets.get('GMAIL_ADDRESS', '')
            settings.GMAIL_APP_PASSWORD = st.secrets.get('GMAIL_APP_PASSWORD', '')
            print(f"🔑 Loaded Gmail SMTP from secrets: {settings.GMAIL_ADDRESS}")

        # Database settings (Supabase)
        if 'DB_HOST' in st.secrets:
            settings.DB_HOST = st.secrets.get('DB_HOST', 'localhost')
            settings.DB_PORT = int(st.secrets.get('DB_PORT', 5432))
            settings.DB_NAME = st.secrets.get('DB_NAME', 'swavlamban2025')
            settings.DB_USER = st.secrets.get('DB_USER', 'postgres')
            settings.DB_PASSWORD = st.secrets.get('DB_PASSWORD', '')
            print(f"🔑 Loaded database config from secrets: {settings.DB_HOST}")

        print("✅ Successfully loaded configuration from Streamlit secrets")
except Exception as e:
    print(f"⚠️ Streamlit secrets not available: {e}")
    print("Using .env configuration")


# Create directories if they don't exist
def create_directories():
    """Create necessary directories for the application"""
    base_dir = Path(__file__).parent.parent.parent

    # Generated passes directory
    passes_dir = base_dir / settings.PASS_OUTPUT_DIR.lstrip("../")
    passes_dir.mkdir(parents=True, exist_ok=True)

    # Ensure images directory exists
    images_dir = base_dir / settings.IMAGE_ASSETS_DIR.lstrip("../")
    if not images_dir.exists():
        print(f"Warning: Images directory not found at {images_dir}")


# Run on module import
create_directories()
