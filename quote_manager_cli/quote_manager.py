import json
import random
from typing import Any, Optional

from .database import Quote
from .logger_config import error_logger, info_logger


def load_quotes_from_json(file_path: str) -> dict[str, tuple]:
    """Imports quotes from a JSON file into the database."""
    info_logger.info(f"Importing quotes from {file_path}...")

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        error_logger.error(f"Error reading JSON file {file_path}: {e}", exc_info=True)
    except FileNotFoundError as e:
        error_logger.error(f"File not found: {e}", exc_info=True)
    except Exception as e:
        error_logger.error(f"An error occurred: {e}", exc_info=True)
    return {}


def load_quotes_to_db(db: Any, data: dict[str, tuple]) -> int:
    """Loads quotes into the database."""
    info_logger.info("Loading quotes into the database...")
    count = 0
    try:
        for category, quotes in data.items():
            for quote_entry in quotes:
                new_quote = Quote(
                    text=quote_entry.get("quote"),
                    author=quote_entry.get("author"),
                    category=category.lower(),
                )
                db.add(new_quote)
                count += 1
        db.commit()
        info_logger.info(f"{count} Quotes saved to db.")
    except Exception as e:
        db.rollback()
        error_logger.error(f"Error importing quotes from JSON: {e}", exc_info=True)
    finally:
        db.close()
    return count


def add_quote(db: Any, category: str, text: str, author: Optional[str] = None) -> None:
    """Adds a new quote to the database."""
    info_logger.info(f"Adding quote: {text} - {category}...")

    try:
        category = category.lower()  # standardize category
        if author is not None:
            new_quote = Quote(text=text, author=author, category=category)
        else:
            new_quote = Quote(text=text, author="Unknown", category=category)
        db.add(new_quote)
        db.commit()
        info_logger.info("Quote added.")
    except Exception as e:
        db.rollback()
        error_logger.error(f"Error adding quote: {e}", exc_info=True)
    finally:
        db.close()


def list_quotes(db: Any, category: Optional[str] = None) -> list[Quote]:
    """Lists quotes from the database."""
    info_logger.info("Listing quotes...")

    try:
        if category:
            quotes = db.query(Quote).filter_by(category=category.lower()).all()
        else:
            quotes = db.query(Quote).all()
        return quotes
    except Exception as e:
        error_logger.error(f"Error listing quotes: {e}", exc_info=True)
    finally:
        db.close()
    return []


def generate_random_quote(db: Any, category: Optional[str] = None) -> Quote | None:
    """Generates a random quote from the database."""
    info_logger.info("Generating random quote...")

    try:
        if category:
            quotes = db.query(Quote).filter_by(category=category.lower()).all()
        else:
            quotes = db.query(Quote).all()
        if quotes:
            quote = random.choice(quotes)
        else:
            info_logger.info("No quotes found.")
        return quote
    except Exception as e:
        error_logger.error(f"Error generating random quote: {e}", exc_info=True)
    finally:
        db.close()
    return None
