# Quote Manager CLI Tool

## Overview

The Quote Manager CLI Tool is a Python-based command-line interface (CLI) application designed for managing quotes. It provides functionalities to import, generate, add, and list quotes using an intuitive command-line interface. The tool integrates with a database to store and manage quotes, and it supports filtering and logging features.

## Features

- **File Import**: Load quotes from a JSON file and store them in a database.
- **Generate Random Quote**: Retrieve a random quote from the database with an optional category filter.
- **Add New Quote**: Add new quotes to the database with text and category.
- **List Quotes**: List quotes from the database, with optional category filtering.
- **Logging**: Record logs for general and error events.
- **Dev support**: Run make commands for testing and development.

## Requirements

- Python 3.8 or higher
- Poetry (for package management)

To install Poetry, run the command below in your terminal:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Data-Epic/Quote-Manager-CLI-Precious.git)
   cd Quote-Manager-CLI-Precious
   ```

2. **Install Dependencies**

   Ensure Poetry is installed. Then, run:

   ```bash
   poetry install
   ```

3. **Activate the Virtual Environment**

   ```bash
   poetry shell
   ```
4. **(Optional) Set up the database file path**

   By default, the application uses default.db for the database file. To use a
   different file, set the DATABASE_PATH environment variable:

   ```bash
   export DATABASE_PATH=path/to/your/database.db
   ```

   This variable can be set in your .env file or directly in your shell.


## Usage
Below are the main commands of the CLI Tool:

1. **Initialize the Database (do this before using the tool for the first time):**

   ```bash
   quote init
   ```

   You can also specify a custom file path to a json file  of your choice:
   ```bash
   quote init --file path/to/quotes.json
   ```

2. **Generate a random quote. Optionally, filter by category:**

   ```bash
   quote generate
   quote generate --category "Motivation"
   ```

3. **Add a New Quote. Provide the category, text, and author:**

   ```bash
   quote add --category "Wisdom" --text "Patience is a virtue." --author "Anonymous"
   ```

4. **List quotes. Optionally, filter by category:**

   ```bash
   quote list
   quote list --category "Humor"
   ```

## Project Structure
```
Quote-Manager-CLI-Precious/
│
├── quote_manager_cli/
│   ├── __init__.py
│   ├── cli.py
│   ├── database.py
│   ├── logger_config.py
│   └── quote_manager.py
│
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_database.py
│   └── test_quote_manager.py
│
├── __init__.py
├── categoty.json
├── Makefile
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Testing and Development 

### Using a test database

During development or testing, it is advised you use a different database file. You can set the DATABASE_PATH environment variable to a different path to use a separate database.

### Makefile Commands

This project includes a Makefile with various commands for managing the development environment. Here are the available commands.

```bash
Available make commands:

make help          # Displays available commands
make setup         # Setup virtual environment and install dependencies
make test          # Run tests
make lint          # Run linter
make format        # Format code
make install       # Install dependencies
make clean         # Cleans up temporary and test files and directories
make type_check	   # Run mypy to type check
make build     	   # Build the package
make publish   	   # Publish the package
make all_checks    # Run tests,  formatter, type check, linter, and clean
```
### Logging

Logs are generated in the following files:

- **General Log**: `/var/log/quote_manager.log`
- **Error Log**: `/var/log/quote_manager-error.log`

Ensure you have the necessary permissions to write to these log files.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.

## Acknowledgment

- Data source: The default quotes used in this project are sourced from [GitHub ReadMe Quotes](https://github.com/shravan20/github-readme-quotes/blob/main/customQuotes/category.json), specifically the category.json file.

