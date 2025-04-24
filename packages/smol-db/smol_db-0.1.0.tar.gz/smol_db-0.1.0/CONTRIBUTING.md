# Contributing to smol-db

Thank you for your interest in contributing to smol-db! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/smol-data/smol-db.git
   cd smol-db
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

We use:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run the formatters:
```bash
black .
isort .
```

Run the linters:
```bash
flake8
mypy .
```

## Testing

Run tests with pytest:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=smol_db
```

### Documentation

- Update docstrings for any modified code
- Update README.md if adding new features
- Add examples for new functionality

### Pull Request Process

1. Create a new branch for your feature/fix
2. Make your changes
3. Run tests and ensure they pass
4. Update documentation
5. Submit a pull request

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test changes
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

## Project Structure

```
smol-db/
├── smol_db/       # Main package
│   ├── __init__.py     # Package initialization
│   └── core.py         # Core functionality
├── tests/             # Test files
├── examples/          # Example scripts
├── docs/              # Documentation
├── pyproject.toml     # Project configuration
├── README.md          # Project documentation
├── LICENSE            # MIT License
└── CONTRIBUTING.md    # This file
```

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.