from sqlalchemy import (
    inspect,
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Sequence,
)
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
from typing import Any, Type
import os
import sys
from .logger_config import info_logger, error_logger


# Fetch database path from environment variable, with a default fallback
DATABASE_FILE = os.getenv(
    "DATABASE_PATH", os.path.join(os.path.dirname(__file__), "quotes.db")
)

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


def create_session(engine: Any) -> Session:
    """Creates and returns a new database session."""
    try:
        SessionLocal = sessionmaker(bind=engine)
        info_logger.info("Database session created.")
        return SessionLocal()
    except Exception as e:
        error_logger.error(f"Error creating session: {e}", exc_info=True)
    
def drop_existing_table(engine: Any) -> None:
    """Drops the existing quotes table."""
    try:
        Base.metadata.drop_all(tables=[Quote.__table__], bind=engine)
        info_logger.info("Existing table dropped.")
    except Exception as e:
        error_logger.error(f"Error dropping table: {e}", exc_info=True)


def init_db(db_url: str = DATABASE_URL) -> Session:
    """Sets up the quotes database and connects to it"""
    info_logger.info("Setting up database...")
    try:
        engine = create_engine(db_url)
        inspector = inspect(engine)
        if "quotes" in inspector.get_table_names():
            drop_existing_table(engine)

        Base.metadata.create_all(engine)
        info_logger.info("Database setup complete.")

        conn = create_session(engine)
        return conn
    except Exception as e:
        error_logger.error(f"Error setting up database: {e}", exc_info=True)
        

def get_db_conn(url: str = DATABASE_URL, db_file: str = DATABASE_FILE) -> Session:
    """Create connection to an existing database"""
    try:
        if not os.path.exists(db_file):
            error_logger.error(
                "Database file does not exist. \
                    Initialize database with `quote init`"
            )
            sys.exit("Database file does not exist. Run `quote init`. Exiting program.")
        else:
            engine = create_engine(url)
            conn = create_session(engine)
            info_logger.info("Connected to Database")
            return conn
    except Exception as e:
        error_logger.error(f"Error connecting to database: {e}", exc_info=True)


