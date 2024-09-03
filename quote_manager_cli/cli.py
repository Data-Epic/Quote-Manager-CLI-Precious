import click
from quote_manager import load_quotes_from_json, load_quotes_to_db, add_quote, list_quotes, generate_random_quote
from database import init_db, get_db_conn
from typing import Optional


@click.group()
def cli() -> None:
    pass

@cli.command()
@click.option('-f', '--file', default='category.json', help='Path to the JSON file containing quotes.')
def init(file : str) -> None:
    """Initialize the database with quotes from a JSON file."""
    init_conn = init_db()
    data = load_quotes_from_json(file)
    load_quotes_to_db(init_conn, data)
    print(f'{len(data)} quotes added')

@cli.command()
@click.option('--category', help='Category of the quote.')
@click.option('--text', help='Text of the quote.')
@click.option('--author', help='Author of the quote.')
def add(category: str, text: str, author: Optional[str] = None) -> None:
    """Add a new quote to the database."""
    add_quote(get_db_conn(), category, text, author)
    print(f"Quote added: {text} - {category}")

@cli.command()
@click.option('--category', help='Category of the quotes.')
def list(category: Optional[str] = None) -> None:
    """List quotes from the database."""
    quotes = list_quotes(get_db_conn(), category)
    for i, quote in enumerate(quotes[:5]):
        print(f"{i+1}. {quote.text} - {quote.author}")

@cli.command()
@click.option('--category', help='Category of the quote.')
def generate(category: Optional[str] = None) -> None:
    """Generate a random quote from the database."""
    quote = generate_random_quote(get_db_conn(), category)
    if quote:
        print(f"Quote: {quote.text} - {quote.author}")
    else:
        print("No quotes found.")

if __name__ == "__main__":
    cli()