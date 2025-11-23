"""
Database connection and session management
Uses SQLAlchemy with PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from .config import settings

# Create SQLAlchemy engine
# Automatically detect: PostgreSQL (production) or SQLite (local development)

# Check if PostgreSQL credentials are configured
import os
use_postgresql = os.getenv("DB_HOST") and os.getenv("DB_NAME")

if use_postgresql:
    # Production: Use PostgreSQL (Streamlit Cloud + external database)
    SQLALCHEMY_DATABASE_URL = settings.database_url
    print(f"🗄️  Using PostgreSQL database: {settings.DB_HOST}")
else:
    # Local development: Use SQLite
    from pathlib import Path
    DB_PATH = Path(__file__).parent.parent.parent.parent / "swavlamban2025.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    print(f"🗄️  Using SQLite database: {DB_PATH}")

# Configure engine with appropriate settings
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    # SQLite requires check_same_thread=False for multi-threaded apps
    connect_args = {"check_same_thread": False}
    engine_kwargs = {}
else:
    # PostgreSQL (Supabase) requires SSL and specific pooler settings
    connect_args = {"sslmode": "require"}
    # Disable prepared statements for Supabase transaction pooler compatibility
    # Transaction pooler (port 6543) does not support prepared statements
    engine_kwargs = {
        "pool_pre_ping": True,  # Test connections before using
        "pool_size": 5,  # Number of connections to keep open
        "max_overflow": 10  # Max additional connections
    }

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    **engine_kwargs if use_postgresql else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    Yields a database session and closes it after use

    Usage:
        @app.get("/users/")
        def read_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database - create all tables
    Should be called on application startup
    """
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized: {SQLALCHEMY_DATABASE_URL}")


def drop_db() -> None:
    """
    Drop all database tables
    ⚠️ USE WITH CAUTION - Only for development/testing
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All database tables dropped")
