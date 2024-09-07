import os
import sys
from datetime import datetime
from typing import Any, Optional, Type

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, Sequence, String, create_engine, inspect
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .logger_config import error_logger, info_logger

load_dotenv()

# Fetch database path from environment variable, with a default fallback
DATABASE_FILE = os.getenv("DATABASE_PATH", "default.db")
DATABASE_URL = f"duckdb:///{DATABASE_FILE}"

Base: Type[Any] = declarative_base()


# Define the Quote model
class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, Sequence("id"), primary_key=True)
    text = Column(String, index=True)
    author = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.now)


def get_engine(url: str = DATABASE_URL) -> Any:
    """Creates and returns a new database engine."""
    try:
        engine = create_engine(url)
        return engine
    except Exception as e:
        error_logger.error(f"Error creating engine: {e}", exc_info=True)
    return None


def create_session(engine: Any) -> Optional[Session]:
    """Creates and returns a new database session."""
    try:
        SessionLocal = sessionmaker(bind=engine)
        info_logger.info(f"Connection to {DATABASE_FILE} database established")
        return SessionLocal()
    except Exception as e:
        error_logger.error(f"Error creating session: {e}", exc_info=True)
    return None


def drop_existing_table(engine: Any) -> None:
    """Drops the existing quotes table."""
    try:
        Base.metadata.drop_all(tables=[Quote.__table__], bind=engine)
        info_logger.info("Existing table dropped.")
    except Exception as e:
        error_logger.error(f"Error dropping table: {e}", exc_info=True)


def init_db(db_url: str = DATABASE_URL) -> Optional[Session]:
    """Sets up the quotes database and connects to it"""
    info_logger.info("Setting up database...")
    try:
        engine = get_engine(db_url)
        inspector = inspect(engine)
        if "quotes" in inspector.get_table_names():
            drop_existing_table(engine)

        Base.metadata.create_all(engine)
        info_logger.info("Database setup complete.")

        conn = create_session(engine)
        return conn
    except Exception as e:
        error_logger.error(f"Error setting up database: {e}", exc_info=True)
    return None


def get_db_conn(url: str = DATABASE_URL, db_file: str = DATABASE_FILE) -> Optional[Session]:
    """Create connection to an existing database"""
    try:
        if not os.path.exists(db_file):
            error_logger.error(
                "Database file does not exist. \
                    Initialize database with `quote init`"
            )
            sys.exit(
                "Database file does not exist. \
                     Run `quote init`. Exiting program."
            )
        else:
            engine = get_engine(url)
            conn = create_session(engine)
            info_logger.info("Connected to Database")
            return conn
    except Exception as e:
        error_logger.error(f"Error connecting to database: {e}", exc_info=True)
    return None
