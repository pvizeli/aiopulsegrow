# Contributing to aiopulsegrow

Thank you for your interest in contributing to aiopulsegrow!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aiopulsegrow.git
cd aiopulsegrow
```

2. Install the package in development mode with dev dependencies:
```bash
pip install -e ".[dev]"
```

## Development Workflow

### Running Tests

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=aiopulsegrow --cov-report=html
```

### Code Quality

Format code with ruff:
```bash
ruff format aiopulsegrow tests
```

Lint with ruff:
```bash
ruff check aiopulsegrow tests
```

Type check with mypy:
```bash
mypy aiopulsegrow
```

### Running All Checks

Before submitting a PR, run all checks:
```bash
ruff format aiopulsegrow tests
ruff check aiopulsegrow tests
mypy aiopulsegrow
pytest --cov=aiopulsegrow
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run all code quality checks
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines (enforced by ruff)
- Use type hints for all functions
- Write docstrings for all public methods
- Keep line length to 100 characters
- Use async/await for all asynchronous operations
- Code formatting is handled by ruff (replaces black + isort)

## Testing

- Write tests for all new features
- Maintain test coverage above 95%
- Use pytest fixtures for common setup
- Mock external API calls using aioresponses

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in the present tense (Add, Fix, Update, etc.)
- Keep the first line under 72 characters
- Add detailed description if needed

## Questions?

Feel free to open an issue for any questions or concerns.
