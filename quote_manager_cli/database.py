import logging
from sqlalchemy import inspect, create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
from typing import Any, Type, Generator
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()




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

def init_db() -> Any:
    """Sets up the qu(db_path=DATotes_manager database"""
    logger.info("Setting up database...")
    try:
        engine = create_engine(DATABASE_URL)
        
        inspector = inspect(engine)
        if 'quotes' in inspector.get_table_names():
            Base.metadata.drop_all(tables=[Quote.__table__], bind=engine)
            logger.info("Existing table dropped.")
        
        Base.metadata.create_all(engine)
        logger.info("Database setup complete.")
        return engine
    except Exception as e:
        logger.error(f"Error setting up database: {e}", exc_info=True)
        raise

def create_session(engine:  Any) -> Session:
    """Creates and returns a new database session."""
    logger.info("Creating a new database session...")
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
    except Exception as e:
        logger.error(f"Error creating session: {e}", exc_info=True)
        raise

def import_quotes_from_json(file_path: str) -> dict[str, tuple]:
    """Imports quotes from a JSON file into the database."""
    logger.info(f"Importing quotes from {file_path}...")
    
    try:
        with open(file_path, 'r') as f:
                    data = json.load(f)
                    return data
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise
    
def load_quotes_to_db(data, db):
    with db as session:
        try:
            for category, quotes in data.items():
                for quote_entry in quotes:
                    new_quote = Quote(
                        text=quote_entry.get('quote'),
                        author=quote_entry.get('author'),
                        category=category
                    )

                    session.add(new_quote)
            
            session.commit()
            logger.info(f"Quotes saved to db.")
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing quotes from JSON: {e}", exc_info=True)
            raise
        finally:
            session.close()
            logger.info("Database session closed.")

if __name__ == "__main__":
    data = import_quotes_from_json('category.json')
    db = create_session(init_db())
    load_quotes_to_db(data, db)


