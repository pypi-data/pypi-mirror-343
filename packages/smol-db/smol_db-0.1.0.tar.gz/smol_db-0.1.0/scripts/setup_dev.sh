#!/bin/bash

# Exit on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install poetry if not installed
if ! command -v poetry &> /dev/null; then
    echo "Installing poetry..."
    curl -sSL https://install.python-poetry.org | python -
fi

# Install dependencies
echo "Installing dependencies..."
poetry install --extras dev

# Verify pydantic installation
echo "Verifying pydantic installation..."
python -c "import pydantic; print(f'Pydantic version: {pydantic.__version__}')"

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Create data directory
echo "Creating data directory..."
mkdir -p data

# Run tests to verify setup
echo "Running tests..."
pytest tests/

echo "Development environment setup complete!"
echo "To activate the virtual environment, run: source .venv/bin/activate"