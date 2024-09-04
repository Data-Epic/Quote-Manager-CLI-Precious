import click
import json
import os
from .quote_manager import (
    load_quotes_from_json,
    load_quotes_to_db,
    add_quote,
    list_quotes,
    generate_random_quote
)
from .database import init_db, get_db_conn
from typing import Optional
from .logger_config import info_logger, error_logger 


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option(
    "-f",
    "--file",
    default="category.json",
    help="Path to the JSON file containing quotes.",
)
def init(file: str) -> None:
    """Initialize the database with quotes from a JSON file."""
    if not os.path.exists(file):
        click.echo(f"Error: {file} does not exist. Please enter a valid json file path.")
        error_logger.error(f"Error: {file} does not exist", exc_info=True)
        return

    try:    
        data = load_quotes_from_json(file)
        if not data:
            click.echo(f"Error: {file} is empty or is not a valid JSON file.")
            return
             
        click.echo(f"Initializing database with quotes from {file}...")
        init_conn = init_db()
        count = load_quotes_to_db(init_conn, data)
        click.echo(f"{count} quotes added")
    except Exception as e:
        error_logger.error(f"Error initializing database: {e}", exc_info=True)
        click.echo(f"Error initializing database: Database initialization failed")


@cli.command()
@click.option("--category", help="Category of the quote.")
@click.option("--text", help="Text of the quote.")
@click.option("--author", help="Author of the quote.")
def add(category: str, text: str, author: Optional[str] = None) -> None:
    """Add a new quote to the database."""
    click.echo(f"Adding new quote: {text} - {category}")
    try:
        add_quote(get_db_conn(), category, text, author)
        click.echo("Quote added successfully.")
    except Exception as e:
        error_logger.error(f"Error adding quote: {e}", exc_info=True)


@cli.command()
@click.option("-c", "--category", help="Category of the quotes.")
def list(category: Optional[str] = None) -> None:
    """List quotes from the database."""
    click.echo(f"Listing quotes for category: {category}")
    try:
        quotes = list_quotes(get_db_conn(), category)
        if len(quotes) == 0:
            click.echo(f"No quotes found in {category}")
            info_logger.info(f"No quotes found in {category}")
            return
        for i, quote in enumerate(quotes[:5]):
            click.echo(f"{i+1}. {quote.text} - {quote.author}")
        info_logger.info(f"Listed 5 quotes in {category}")
    except Exception as e:
        error_logger.error(f"Error listing quotes: {e}", exc_info=True)



@cli.command()
@click.option("-c", "--category", help="Category of the quote.")
def generate(category: Optional[str] = None) -> None:
    """Generate a random quote from the database."""
    click.echo(f"Generating quote for category: {category}")
    try:
        quote = generate_random_quote(get_db_conn(), category)
        if quote:
            click.echo(f"Quote: {quote.text} - {quote.author}")
            info_logger.info(f"Generated quote: {quote.text} - {quote.author}")
        else:
            click.echo("No quotes found.")
            info_logger.info("No quotes found.")
    except Exception as e:
        error_logger.error(f"Error generating quote: {e}", exc_info=True)



if __name__ == "__main__":
    cli()

