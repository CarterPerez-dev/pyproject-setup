"""
AngelaMos | 2025
cli.py
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from . import __version__
from .generator import (
    ProjectConfig,
    write_publish_workflow,
    write_pyproject,
    write_style_yapf,
)
from .presets import PRESETS


app = typer.Typer(
    name = "pyproject-setup",
    help =
    "Scaffold pyproject.toml with pre-configured linting and tooling.",
    rich_markup_mode = "rich",
    no_args_is_help = True,
)
console = Console()


def version_callback(value: bool) -> None:
    """
    Display version and exit.
    """
    if value:
        console.print(
            f"[bold cyan]pyproject-setup[/bold cyan] v{__version__}"
        )
        raise typer.Exit()


@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        callback = version_callback,
        is_eager = True,
        help = "Show version and exit.",
    ),
) -> None:
    """
    pyproject-setup - Scaffold pyproject.toml files.
    """
    pass


@app.command()
def init(
    name: str | None = typer.Option(
        None,
        "--name",
        "-n",
        help = "Project name"
    ),
    description: str | None = typer.Option(
        None,
        "--description",
        "-d",
        help = "Project description"
    ),
    preset: str | None = typer.Option(
        None,
        "--preset",
        "-p",
        help = "Project preset (fastapi-backend, library, cli-tool)",
    ),
    python: str = typer.Option(
        ">=3.12",
        "--python",
        help = "Python version requirement"
    ),
    package_path: str = typer.Option(
        "src",
        "--package-path",
        help = "Package source path"
    ),
    repository: str | None = typer.Option(
        None,
        "--repository",
        "-r",
        help = "Repository URL"
    ),
    homepage: str | None = typer.Option(
        None,
        "--homepage",
        help = "Homepage URL"
    ),
    workflow: bool = typer.Option(
        True,
        "--workflow/--no-workflow",
        help = "Add PyPI workflow"
    ),
    output: Path = typer.Option(
        Path(),
        "--output",
        "-o",
        help = "Output directory"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help = "Overwrite existing files"
    ),
    yapf: bool = typer.Option(
        False,
        "--yapf/--no-yapf",
        help = "Add .style.yapf config file"
    ),
) -> None:
    """
    [bold green]Initialize[/bold green] a new pyproject.toml with pre-configured tooling.

    Run interactively or pass flags for automation.
    """
    console.print()
    console.print(
        Panel(
            "[bold cyan]pyproject-setup[/bold cyan] - Project Scaffolder",
            border_style = "cyan",
        )
    )
    console.print()

    pyproject_path = output / "pyproject.toml"
    if (
        pyproject_path.exists()
        and not force
        and not Confirm.ask(
            f"[yellow]pyproject.toml already exists at {output}. Overwrite?[/yellow]"
        )
    ):
        console.print("[red]Aborted.[/red]")
        raise typer.Exit(1)

    if name is None:
        name = Prompt.ask(
            "[bold]Project name[/bold]",
            default = output.resolve().name
        )

    if description is None:
        description = Prompt.ask("[bold]Description[/bold]", default = "")

    if preset is None:
        preset_choices = list(PRESETS.keys())
        console.print("\n[bold]Available presets:[/bold]")
        for i, p in enumerate(preset_choices, 1):
            preset_obj = PRESETS[p]
            console.print(
                f"  [cyan]{i}[/cyan]. {p} - {preset_obj.description}"
            )

        while True:
            choice = Prompt.ask(
                "\n[bold]Select preset[/bold]",
                default = "1",
            )
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(preset_choices):
                    preset = preset_choices[idx]
                    break
            except ValueError:
                if choice in preset_choices:
                    preset = choice
                    break
            console.print("[red]Invalid choice. Try again.[/red]")

    if preset not in PRESETS:
        console.print(f"[red]Unknown preset: {preset}[/red]")
        raise typer.Exit(1)

    python_ver = Prompt.ask(
        "[bold]Python version[/bold]",
        default = python
    )
    pkg_path = Prompt.ask(
        "[bold]Package path[/bold]",
        default = package_path
    )

    add_workflow = workflow
    if workflow:
        add_workflow = Confirm.ask(
            "[bold]Add PyPI publish workflow?[/bold]",
            default = True
        )

    add_yapf = yapf
    if not yapf:
        add_yapf = Confirm.ask(
            "[bold]Add .style.yapf config?[/bold]",
            default = False
        )

    repo = repository
    if repo is None:
        repo = Prompt.ask(
            "[bold]Repository URL[/bold] (optional)",
            default = ""
        )
        if not repo:
            repo = None

    home = homepage
    if home is None:
        home = Prompt.ask(
            "[bold]Homepage URL[/bold] (optional)",
            default = ""
        )
        if not home:
            home = None

    console.print()

    config = ProjectConfig(
        name = name,
        description = description,
        python_version = python_ver,
        package_path = pkg_path,
        preset = preset,
        repository = repo,
        homepage = home,
    )

    with console.status(
            "[bold green]Generating pyproject.toml...[/bold green]"):
        pyproject_file = write_pyproject(config, output)
        console.print(f"[green]Created[/green] {pyproject_file}")

        if add_workflow:
            workflow_file = write_publish_workflow(name, output)
            console.print(f"[green]Created[/green] {workflow_file}")

        if add_yapf:
            yapf_file = write_style_yapf(output)
            console.print(f"[green]Created[/green] {yapf_file}")

    console.print()
    console.print(
        Panel(
            f"[bold green]Done![/bold green] Project [cyan]{name}[/cyan] initialized.\n\n"
            f"Next steps:\n"
            f"  1. Create [cyan]{pkg_path}/[/cyan] directory\n"
            f"  2. [dim]pip install -e \".[dev]\"[/dim]\n"
            f"  3. Start coding!",
            title = "Success",
            border_style = "green",
        )
    )


if __name__ == "__main__":
    app()
