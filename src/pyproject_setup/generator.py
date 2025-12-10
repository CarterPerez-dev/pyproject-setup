"""
AngelaMos | 2025
generator.py
"""

from typing import Any
from pathlib import Path
from dataclasses import dataclass

import tomli_w

from .presets import (
    PRESETS,
    Preset,
    get_mypy_config,
    get_pylint_config,
    get_pytest_config,
    get_ruff_config,
    get_ty_config,
    get_coverage_config,
    get_pydantic_mypy_config,
)


@dataclass
class ProjectConfig:
    """
    User provided project configuration
    """
    name: str
    description: str
    version: str = "0.1.0"
    python_version: str = ">=3.12"
    package_path: str = "src"
    preset: str = "fastapi-backend"
    homepage: str | None = None
    repository: str | None = None
    author_name: str | None = None
    author_email: str | None = None


PUBLISH_WORKFLOW = '''name: Publish to PyPI

on:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  pypi-publish:
    name: Upload release to PyPI
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/$PROJECT_NAME
    permissions:
      id-token: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
'''

STYLE_YAPF = '''[style]
based_on_style = pep8
column_limit = 75
indent_width = 4
continuation_indent_width = 4
indent_closing_brackets = false
dedent_closing_brackets = true
indent_blank_lines = false
spaces_before_comment = 2
spaces_around_power_operator = false
spaces_around_default_or_named_assign = true
space_between_ending_comma_and_closing_bracket = false
space_inside_brackets = false
spaces_around_subscript_colon = true
blank_line_before_nested_class_or_def = false
blank_line_before_class_docstring = false
blank_lines_around_top_level_definition = 2
blank_lines_between_top_level_imports_and_variables = 2
blank_line_before_module_docstring = false
split_before_logical_operator = true
split_before_first_argument = true
split_before_named_assigns = true
split_complex_comprehension = true
split_before_expression_after_opening_paren = false
split_before_closing_bracket = true
split_all_comma_separated_values = true
split_all_top_level_comma_separated_values = false
coalesce_brackets = false
each_dict_entry_on_separate_line = true
allow_multiline_lambdas = false
allow_multiline_dictionary_keys = false
split_penalty_import_names = 0
join_multiple_lines = false
align_closing_bracket_with_visual_indent = true
arithmetic_precedence_indication = false
split_penalty_for_added_line_split = 275
use_tabs = false
split_before_dot = false
split_arguments_when_comma_terminated = true
i18n_function_call = ['_', 'N_', 'gettext', 'ngettext']
i18n_comment = ['# Translators:', '# i18n:']
split_penalty_comprehension = 80
split_penalty_after_opening_bracket = 280
split_penalty_before_if_expr = 0
split_penalty_bitwise_operator = 290
split_penalty_logical_operator = 0
'''


def build_pyproject(config: ProjectConfig) -> dict[str, Any]:
    """
    Build complete pyproject.toml structure from config
    """
    preset: Preset = PRESETS[config.preset]

    project: dict[str,
                  Any] = {
                      "name": config.name,
                      "version": config.version,
                      "description": config.description,
                      "requires-python": config.python_version,
                      "dependencies": preset.dependencies.copy(),
                  }

    if preset.dev_dependencies:
        project["optional-dependencies"] = {
            "dev": preset.dev_dependencies.copy()
        }

    urls: dict[str, str] = {}
    if config.homepage:
        urls["Homepage"] = config.homepage
    if config.repository:
        urls["Repository"] = config.repository
        urls["Issues"] = f"{config.repository}/issues"
        urls["Changelog"] = f"{config.repository}/blob/main/CHANGELOG.md"
    if urls:
        project["urls"] = urls

    if config.author_name and config.author_email:
        project["authors"] = [
            {
                "name": config.author_name,
                "email": config.author_email
            }
        ]

    pyproject: dict[str,
                    Any] = {
                        "project": project,
                        "build-system": {
                            "requires": ["hatchling"],
                            "build-backend": "hatchling.build",
                        },
                        "tool": {
                            "hatch": {
                                "build": {
                                    "targets": {
                                        "wheel": {
                                            "packages":
                                            [config.package_path]
                                        }
                                    }
                                }
                            },
                            "ruff":
                            get_ruff_config(config.package_path),
                            "mypy":
                            get_mypy_config(config.package_path),
                            "pydantic-mypy":
                            get_pydantic_mypy_config(),
                            "pylint":
                            get_pylint_config(config.package_path),
                            "pytest": {
                                "ini_options": get_pytest_config()
                            },
                            "coverage":
                            get_coverage_config(config.package_path),
                            "ty":
                            get_ty_config(config.package_path),
                        },
                    }

    if preset.entry_point:
        pyproject["project"]["scripts"] = {
            config.name:
            f"{config.package_path.replace('/', '.')}.{preset.entry_point}"
        }

    return pyproject


def write_pyproject(config: ProjectConfig, output_dir: Path) -> Path:
    """
    Generate and write pyproject.toml file
    """
    pyproject = build_pyproject(config)
    output_path = output_dir / "pyproject.toml"

    with output_path.open("wb") as f:
        tomli_w.dump(pyproject, f)

    return output_path


def write_publish_workflow(project_name: str, output_dir: Path) -> Path:
    """
    Generate and write GitHub Actions publish workflow
    """
    workflow_dir = output_dir / ".github" / "workflows"
    workflow_dir.mkdir(parents = True, exist_ok = True)

    workflow_content = PUBLISH_WORKFLOW.replace(
        "$PROJECT_NAME",
        project_name
    )
    output_path = workflow_dir / "publish.yml"

    with output_path.open("w") as f:
        f.write(workflow_content)

    return output_path


def write_style_yapf(output_dir: Path) -> Path:
    """
    Generate and write .style.yapf file
    """
    output_path = output_dir / ".style.yapf"

    with output_path.open("w") as f:
        f.write(STYLE_YAPF)

    return output_path
