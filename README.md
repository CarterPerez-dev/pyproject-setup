# pyproject-setup

CLI tool to scaffold `pyproject.toml` files with pre-configured linting and tooling.

## Installation

```bash
pip install pyproject-setup
```

## Usage

```bash
# Interactive mode
pyproject-setup init
# or
pps init

# With flags
pps init --preset fastapi-backend --name my-api

# All flags (non-interactive)
pps init \
  --preset fastapi-backend \
  --name my-api \
  --description "My API" \
  --python ">=3.12" \
  --package-path src \
  --no-workflow
```

## Presets

- **fastapi-backend** - FastAPI + SQLAlchemy + JWT auth + full dev tooling
- **library** - Python library with no runtime deps
- **cli-tool** - Typer + Rich CLI application

All presets include ruff, mypy, pylint, pytest, ty, and coverage configurations.
