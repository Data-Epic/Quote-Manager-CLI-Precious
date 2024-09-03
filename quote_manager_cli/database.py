import logging
from sqlalchemy import inspect, create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
from typing import Any, Type, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# # Configure the logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('/var/log/quote_manager.log'),  # Info log file
#         logging.FileHandler('/var/log/quote_manager-error.log'),  # Error log file
#         logging.StreamHandler()  # Output to console
#     ]
# )

# # Create a custom logger
# logger = logging.getLogger()

# Fetch database path from environment variable, with a default fallback
DATABASE_FILE = os.getenv('DATABASE_PATH', os.path.join(os.path.dirname(__file__), 'quotes.db'))

DATABASE_URL = f'duckdb:///{DATABASE_FILE}'

Base: Type[Any] = declarative_base()

# Define the Quote model
class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, Sequence('id'), primary_key=True)
    text = Column(String, index=True)
    author = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  


def create_session(engine: Any) -> Session:
    """Creates and returns a new database session."""
    logger.info("Creating a new database session...")
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
    except Exception as e:
        logger.error(f"Error creating session: {e}", exc_info=True)
        raise

def init_db() -> Session:
    """Sets up the quotes database and connects to it"""
    logger.info("Setting up database...")
    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)
        if 'quotes' in inspector.get_table_names():
            Base.metadata.drop_all(tables=[Quote.__table__], bind=engine)
            logger.info("Existing table dropped.")
        
        Base.metadata.create_all(engine)
        logger.info("Database setup complete.")
        
        conn = create_session(engine)
        return conn
    
    except Exception as e:
        logger.error(f"Error setting up database: {e}", exc_info=True)
        raise

def get_db_conn(url: Optional[str] = DATABASE_URL) -> Session:
    """Create connection to a database"""
    try:
        if not os.path.exists(DATABASE_FILE):
            logger.info("Database file does not exist. Initializing database...")
            conn = init_db()
        else:
            engine = create_engine(url)
            conn = create_session(engine)
        logger.info("Connected to Database")  
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}", exc_info=True)
        raise
