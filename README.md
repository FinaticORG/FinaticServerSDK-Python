# Python

Python SDK for Finatic Server API

## Installation

```bash
npm install @finatic/server-node
```

## Quick Start

```typescript
import { FinaticServer} from '@finatic/server-node';

// TODO: Add example usage
```

## Documentation

Full documentation is available at [docs.finatic.com](/server/typescript).

## Development

```bash
# Install dependencies
uv sync --dev

# Build
uv build

# Run tests
pytest

# Format code
black src tests
isort src tests

# Lint
flake8 src tests
```

## Quality Checks

Run all quality checks to ensure code quality:

```bash
# Run all quality checks (format, lint, type check, import check)
python quality_check.py
# or
uv run python quality_check.py

# Fix all auto-fixable issues (format, import sort)
python quality_check.py --fix
# or
uv run python quality_check.py --fix
```

Individual quality checks:

```bash
# Format check (black)
black --check src tests
# Format fix (modifies files)
black src tests

# Import sort check
isort --check-only src tests
# Import sort fix (modifies files)
isort src tests

# Lint & import check (flake8)
flake8 src tests

# Type check (mypy)
mypy src
```

## License

MIT
