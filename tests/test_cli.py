import json
import os
import pytest
from click.testing import CliRunner
from quote_manager_cli.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def test_quotes():
    data = {
        "category1": [
            {"quote": "Quote 1", "author": "Author 1"},
            {"quote": "Quote 2", "author": "Author 2"},
        ],
        "category2": [
            {"quote": "Quote 3", "author": "Author 3"},
            {"quote": "Quote 4", "author": "Author 4"},
        ],
    }

    with open("test_quotes.json", "w") as f:
        json.dump(data, f)

    yield "test_quotes.json"
    if os.path.exists("test_quotes.json"):
        os.remove("test_quotes.json")


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture
def init_db(runner, test_quotes):
    test_file = test_quotes
    result = runner.invoke(cli, ["init", "--file", test_file])
    assert result.exit_code == 0
    yield


def test_init_with_valid_file(runner, test_quotes):
    test_file = test_quotes
    result = runner.invoke(cli, ["init", "--file", test_file])
    assert result.exit_code == 0
    assert "Initializing database with quotes from test_quotes.json..." in result.output
    assert "4 quotes added" in result.output


def test_init_with_empty_file(runner):
    with open("empty_quotes.json", "w"):
        pass
    result = runner.invoke(cli, ["init", "--file", "empty_quotes.json"])
    assert result.exit_code == 0
    assert (
        "Error: empty_quotes.json is empty or is not a valid JSON file."
        in result.output
    )
    if os.path.exists("empty_quotes.json"):
        os.remove("empty_quotes.json")


def test_init_with_nonexistent_file(runner):
    result = runner.invoke(cli, ["init", "--file", "nonexistent_quotes.json"])
    assert result.exit_code == 0
    assert "Error: nonexistent_quotes.json does not exist." in result.output


def test_init_with_invalid_file(runner):
    with open("invalid_quotes.txt", "w") as f:
        f.write("This is not a valid json file.")
    result = runner.invoke(cli, ["init", "--file", "invalid_quotes.txt"])
    assert result.exit_code == 0
    assert (
        "Error: invalid_quotes.txt is empty or is not a valid JSON file."
        in result.output
    )
    if os.path.exists("invalid_quotes.txt"):
        os.remove("invalid_quotes.txt")


def test_init_with_exception(runner, monkeypatch, test_quotes):
    def mock_init_db():
        raise Exception("Database initialization failed")

    monkeypatch.setattr("quote_manager_cli.cli.init_db", mock_init_db)

    test_file = test_quotes
    result = runner.invoke(cli, ["init", "--file", test_file])
    assert result.exit_code == 0
    assert "Error: Database initialization failed" in result.output


def test_add_quote(runner, init_db):
    result = runner.invoke(
        cli, ["add", "--category", "category", "--text", "text", "--author", "author"]
    )
    assert result.exit_code == 0
    assert "Adding new quote: text - category" in result.output
    assert "Quote added successfully." in result.output


def test_generate_quote(runner, init_db):
    # Generate a random quote
    result = runner.invoke(cli, ["generate", "--category", "category1"])
    assert result.exit_code == 0
    assert "Quote:" in result.output
    assert any(q in result.output for q in ["Quote 1", "Quote 2"])

    # Check for no quotes in a category
    result = runner.invoke(cli, ["generate", "--category", "nonexistent_category"])
    assert result.exit_code == 0
    assert "No quotes found." in result.output


def test_list_quotes(runner, init_db):
    # List quotes from a category
    result = runner.invoke(cli, ["list", "--category", "category1"])
    assert result.exit_code == 0
    assert "Listing quotes for category: category1" in result.output
    assert any(q in result.output for q in ["Quote 1", "Quote 2"])

    # Check for no quotes in a category
    result = runner.invoke(cli, ["list", "--category", "nonexistent_category"])
    assert result.exit_code == 0
    assert "No quotes found in nonexistent_category" in result.output
