"""
AngelaMos | 2025
presets.py
"""

from typing import Any
from dataclasses import (
    field,
    dataclass,
)


@dataclass
class Preset:
    """
    Configuration preset for pyproject.toml generation
    """
    name: str
    description: str
    dependencies: list[str] = field(default_factory = list)
    dev_dependencies: list[str] = field(default_factory = list)
    entry_point: str | None = None


FASTAPI_DEPS = [
    "fastapi-cli>=0.0.16,<0.1.0",
    "pydantic>=2.12.5,<3.0.0",
    "pydantic-settings>=2.12.0,<3.0.0",
    "psycopg2-binary>=2.9.11,<3.0.0",
    "sqlalchemy>=2.0.32,<3.0.0",
    "alembic>=1.17.2,<2.0.0",
    "asyncpg>=0.31.0,<1.0.0",
    "python-multipart>=0.0.20,<0.1.0",
    "pyjwt>=2.10.1,<3.0.0",
    "pwdlib[argon2]>=0.3.0,<0.4.0",
    "uuid6>=2025.0.1,<2026.0.0",
    "slowapi>=0.1.9,<0.2.0",
    "redis>=7.1.0,<8.0.0",
    "structlog>=25.5.0,<26.0.0",
    "gunicorn>=23.0.0,<24.0.0",
    "uvicorn[standard]>=0.38.0,<0.39.0",
]

FASTAPI_DEV_DEPS = [
    "pytest>=9.0.2,<10.0.0",
    "pytest-asyncio>=1.3.0,<2.0.0",
    "pytest-cov>=7.0.0,<8.0.0",
    "httpx>=0.28.1,<0.29.0",
    "aiosqlite>=0.21.0,<0.22.0",
    "asgi-lifespan>=2.1.0,<3.0.0",
    "mypy>=1.19.0,<2.0.0",
    "types-redis>=4.6.0.20241004,<5.0.0",
    "ruff>=0.14.8,<0.15.0",
    "ty>=0.0.1a32,<0.1.0",
    "pre-commit>=4.5.0,<5.0.0",
    "pylint>=4.0.4,<5.0.0",
    "pylint-pydantic>=0.4.1,<0.5.0",
    "pylint-per-file-ignores>=3.2.0,<4.0.0",
]

LIBRARY_DEV_DEPS = [
    "pytest>=9.0.2,<10.0.0",
    "pytest-cov>=7.0.0,<8.0.0",
    "httpx>=0.28.1,<0.29.0",
    "mypy>=1.19.0,<2.0.0",
    "ruff>=0.14.8,<0.15.0",
    "ty>=0.0.1a32,<0.1.0",
    "pre-commit>=4.5.0,<5.0.0",
    "pylint>=4.0.4,<5.0.0",
]

CLI_DEPS = [
    "typer>=0.20.0,<0.21.0",
    "rich>=14.2.0,<15.0.0",
]

CLI_DEV_DEPS = [
    "pytest>=9.0.2,<10.0.0",
    "pytest-cov>=7.0.0,<8.0.0",
    "mypy>=1.19.0,<2.0.0",
    "ruff>=0.14.8,<0.15.0",
    "ty>=0.0.1a32,<0.1.0",
    "pre-commit>=4.5.0,<5.0.0",
    "pylint>=4.0.4,<5.0.0",
]

PRESETS: dict[
    str,
    Preset] = {
        "fastapi-backend":
        Preset(
            name = "fastapi-backend",
            description = "FastAPI async backend with SQLAlchemy + JWT",
            dependencies = FASTAPI_DEPS,
            dev_dependencies = FASTAPI_DEV_DEPS,
        ),
        "library":
        Preset(
            name = "library",
            description = "Python library (no runtime deps)",
            dependencies = [],
            dev_dependencies = LIBRARY_DEV_DEPS,
        ),
        "cli-tool":
        Preset(
            name = "cli-tool",
            description = "CLI tool with Typer + Rich",
            dependencies = CLI_DEPS,
            dev_dependencies = CLI_DEV_DEPS,
            entry_point = "main:app",
        ),
    }


def get_ruff_config(package_path: str) -> dict[str, Any]:
    """
    Return ruff configuration section.
    """
    return {
        "target-version": "py312",
        "line-length": 88,
        "src": [package_path],
        "exclude": ["alembic"],
        "lint": {
            "select": [
                "E",
                "W",
                "F",
                "B",
                "C4",
                "UP",
                "ARG",
                "SIM",
                "PTH",
                "RUF",
                "ASYNC",
                "S",
                "N",
            ],
            "ignore": [
                "E501",
                "B008",
                "S101",
                "S104",
                "S105",
                "ARG001",
                "E712",
                "N999",
                "N818",
                "UP046",
                "RUF005",
            ],
            "per-file-ignores": {
                "tests/**/*.py": ["S101",
                                  "ARG001"],
                "conftest.py": ["S107"],
                f"{package_path}/core/rate_limit.py": ["S110"],
                f"{package_path}/config.py": ["F401"],
                f"{package_path}/schemas/**/*.py": ["RUF012"],
            },
        },
    }


def get_mypy_config(package_path: str) -> dict[str, Any]:
    """
    Return mypy configuration section.
    """
    return {
        "python_version":
        "3.12",
        "strict":
        True,
        "warn_return_any":
        True,
        "warn_unused_ignores":
        True,
        "disallow_untyped_defs":
        True,
        "disallow_incomplete_defs":
        True,
        "plugins": ["pydantic.mypy"],
        "exclude": ["alembic"],
        "overrides": [
            {
                "module": ["tests.*",
                           "conftest"],
                "ignore_errors": True
            },
            {
                "module": [f"{package_path}.core.logging"],
                "disable_error_code": ["no-any-return"]
            },
            {
                "module": [
                    "uuid6",
                    "structlog",
                    "structlog.*",
                    "pwdlib",
                    "slowapi",
                    "slowapi.*",
                ],
                "ignore_missing_imports":
                True,
            },
            {
                "module": [f"{package_path}.config"],
                "implicit_reexport": True
            },
            {
                "module": [
                    f"{package_path}.core.enums",
                    f"{package_path}.core.security"
                ],
                "disable_error_code": ["return-value",
                                       "no-any-return"],
            },
            {
                "module": [f"{package_path}.repositories.*"],
                "disable_error_code":
                ["return-value",
                 "no-any-return",
                 "attr-defined"],
            },
            {
                "module": [f"{package_path}.factory"],
                "disable_error_code": ["arg-type"]
            },
        ],
    }


def get_pylint_config(package_path: str) -> dict[str, Any]:
    """
    Return pylint configuration section.
    """
    return {
        "main": {
            "py-version":
            "3.12",
            "jobs":
            4,
            "load-plugins": ["pylint_pydantic",
                             "pylint_per_file_ignores"],
            "persistent":
            True,
            "suggestion-mode":
            True,
            "ignore": [
                "alembic",
                "venv",
                ".venv",
                "__pycache__",
                "build",
                "dist",
                ".git",
                ".pytest_cache",
                ".mypy_cache",
                ".ruff_cache",
            ],
            "ignore-paths": [
                "^alembic/.*",
                "^venv/.*",
                "^.venv/.*",
                "^build/.*",
                "^dist/.*",
            ],
        },
        "messages_control": {
            "disable": [
                "C0103",
                "C0116",
                "C0121",
                "C0301",
                "C0302",
                "C0303",
                "C0304",
                "C0305",
                "C0411",
                "E0401",
                "E1102",
                "E1136",
                "R0801",
                "R0901",
                "R0903",
                "R0917",
                "W0611",
                "W0612",
                "W0613",
                "W0621",
                "W0622",
                "W0718",
            ],
        },
        "pylint-per-file-ignores": {
            "alembic/env.py": "no-member",
            "conftest.py": "import-outside-toplevel",
        },
        "format": {
            "max-line-length": 95
        },
        "design": {
            "max-args": 12,
            "max-attributes": 10,
            "max-branches": 15,
            "max-locals": 20,
            "max-statements": 55,
        },
    }


def get_pytest_config() -> dict[str, Any]:
    """
    Return pytest configuration section.
    """
    return {
        "asyncio_mode": "auto",
        "asyncio_default_fixture_loop_scope": "function",
        "testpaths": ["tests"],
        "addopts": "-ra -q",
        "filterwarnings": ["ignore::DeprecationWarning"],
    }


def get_coverage_config(package_path: str) -> dict[str, Any]:
    """
    Return coverage configuration sections.
    """
    return {
        "run": {
            "branch": True,
            "source": [package_path]
        },
        "report": {
            "exclude_lines": [
                "pragma: no cover",
                "if TYPE_CHECKING:",
                "raise NotImplementedError",
            ],
        },
    }


def get_ty_config(package_path: str) -> dict[str, Any]:
    """
    Return ty (type checker) configuration section.
    """
    return {
        "src": {
            "include": [package_path,
                        "tests"],
            "exclude": ["alembic/versions/**",
                        ".venv/**"],
            "respect-ignore-files": True,
        },
        "environment": {
            "python-version": "3.12",
            "root": [f"./{package_path}"],
            "python": "./.venv",
        },
        "rules": {
            "possibly-missing-attribute": "error",
            "possibly-missing-import": "error",
            "unused-ignore-comment": "warn",
            "redundant-cast": "warn",
            "undefined-reveal": "warn",
        },
        "overrides": [
            {
                "include": ["tests/**"],
                "rules": {
                    "unresolved-reference": "warn",
                    "invalid-argument-type": "warn",
                },
            },
            {
                "include": [
                    f"{package_path}/repositories/**",
                    f"{package_path}/services/**"
                ],
                "rules": {
                    "unresolved-attribute": "warn"
                },
            },
        ],
        "terminal": {
            "error-on-warning": False,
            "output-format": "full"
        },
    }


def get_pydantic_mypy_config() -> dict[str, Any]:
    """
    Return pydantic-mypy plugin configuration.
    """
    return {
        "init_forbid_extra": True,
        "init_typed": True,
        "warn_required_dynamic_aliases": True,
    }
