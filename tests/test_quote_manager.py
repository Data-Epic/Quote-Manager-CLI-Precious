import json
import os
import pytest

from quote_manager_cli.database import Quote, init_db
from quote_manager_cli.quote_manager import (add_quote, generate_random_quote,
                                             list_quotes,
                                             load_quotes_from_json,
                                             load_quotes_to_db)


@pytest.fixture(scope="module")
def test_data():
    return {
        "category1": [
            {"quote": "Quote 1", "author": "Author 1"},
            {"quote": "Quote 2", "author": "Author 2"},
        ],
        "category2": [
            {"quote": "Quote 3", "author": "Author 3"},
            {"quote": "Quote 4", "author": "Author 4"},
        ],
    }


@pytest.fixture(scope="module")
def test_db():
    # Create an in-memory SQLite database for testing
    test_url = "sqlite:///:memory:"
    session = init_db(test_url)
    yield session
    session.close()


def test_load_quotes_from_json(test_data):
    """Test load_quotes_from_json function."""
    file_path = "test_quotes.json"
    data = test_data
    # Save quotes to JSON file
    with open(file_path, "w") as f:
        json.dump(data, f)

    # Load quotes from JSON file
    loaded_data = load_quotes_from_json(file_path)

    assert loaded_data == data

    # Clean up
    os.remove(file_path)


def test_load_quotes_to_db(test_db, test_data):
    """Test load_quotes_to_db function."""
    data = test_data

    load_quotes_to_db(test_db, data)

    # Check if quotes are loaded into the database
    quotes = test_db.query(Quote).all()
    assert len(quotes) == 4
    assert quotes[0].text == "Quote 1"

    test_db.query(Quote).delete()
    test_db.commit()


def test_add_quote(test_db):
    """Test add_quote function."""
    category = "category1"
    text = "Test quote"
    author = "Test author"

    add_quote(test_db, category, text, author)

    # Check if quote is added to the database
    quote = (
        test_db.query(Quote)
        .filter_by(category=category, text=text, author=author)
        .first()
    )
    assert quote is not None

    # Clean up
    test_db.query(Quote).delete()
    test_db.commit()


def test_list_quotes(test_db):
    """Test list_quotes function."""
    category = "category1"
    quotes_data = [
        {"quote": "Quote 1", "author": "Author 1"},
        {"quote": "Quote 2", "author": "Author 2"},
    ]

    # Add quotes to the database
    for quote_data in quotes_data:
        new_quote = Quote(
            text=quote_data["quote"], author=quote_data["author"], category=category
        )
        test_db.add(new_quote)
    test_db.commit()

    # List quotes
    quotes = list_quotes(test_db, category)

    assert len(quotes) == 2

    # Clean up
    test_db.query(Quote).delete()
    test_db.commit()


def test_generate_random_quote(test_db):
    """Test generate_random_quote function."""
    category = "category1"
    quotes_data = [
        {"quote": "Quote 1", "author": "Author 1"},
        {"quote": "Quote 2", "author": "Author 2"},
    ]

    # Add quotes to the database
    for quote_data in quotes_data:
        new_quote = Quote(
            text=quote_data["quote"], author=quote_data["author"], category=category
        )
        test_db.add(new_quote)
    test_db.commit()

    # Generate random quote
    quote = generate_random_quote(test_db, category)

    assert quote is not None

    # Clean up
    test_db.query(Quote).delete()
    test_db.commit()
