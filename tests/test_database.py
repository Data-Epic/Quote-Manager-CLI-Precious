import os
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from quote_manager_cli.database import (Quote, create_session,
                                        drop_existing_table, get_db_conn,
                                        get_engine, init_db)


@pytest.fixture(scope="module")
def test_engine():
    # Create a test engine
    engine = get_engine()
    yield engine


@pytest.fixture(scope="module")
def test_session(test_engine):
    # Create a test session
    session = create_session(test_engine)
    yield session
    session.close()


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")


def test_create_session(test_engine):
    """Test that create_session creates a new database session."""
    session = create_session(test_engine)
    assert isinstance(session, Session)
    session.close()


def test_drop_existing_table(test_engine):
    """Test that drop_existing_table drops the quotes table."""
    # Ensure the table exists first
    init_db(test_engine.url)
    inspector = inspect(test_engine)
    assert "quotes" in inspector.get_table_names()

    # Drop the table
    drop_existing_table(test_engine)
    inspector = inspect(test_engine)
    assert "quotes" not in inspector.get_table_names()


def test_init_db():
    """Test that init_db creates a new database session and sets up the quotes table."""
    db = init_db()
    assert isinstance(db, Session)
    connection = db.bind.connect()
    quote_table_exists = db.bind.dialect.has_table(connection, "quotes")
    assert quote_table_exists
    connection.close()
    db.close()


def test_get_db_conn_creates_session():
    """Test that get_db_conn creates a new database session."""
    conn = get_db_conn()
    assert isinstance(conn, Session)
    conn.close()


def test_get_db_conn_non_existent_db():
    """Test that get_db_conn raises SystemExit for a non-existent database."""
    with pytest.raises(SystemExit):
        get_db_conn("duckdb:///non_existent.db", db_file="non_existent.db")


def test_quote_model(test_session):
    """Test the Quote model."""
    # Create a new quote
    new_quote = Quote(author="Author Name", text="This is a quote.")
    test_session.add(new_quote)
    test_session.commit()

    # Query the quote
    quote = test_session.query(Quote).filter_by(author="Author Name").first()
    assert quote is not None
    assert quote.author == "Author Name"
    assert quote.text == "This is a quote."

    # Clean up
    test_session.delete(quote)
    test_session.commit()
