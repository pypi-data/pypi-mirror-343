import pathlib
import subprocess

import typer

app = typer.Typer()


@app.command()
def lint(path: pathlib.Path = typer.Option(".")) -> None:
    config = pathlib.Path(__file__).parent / "configs"

    commands = [
        ["isort", str(path), "--settings-path", str(config)],
        ["ruff", "format", str(path), "--no-cache", "--config", str(config / "ruff.toml")],
        ["mypy", str(path), "--config-file", str(config / "mypy.ini")],
        ["radon", "cc", str(path), "-a", "-nc"],
    ]

    for command in commands:
        typer.echo(f"Running {' '.join(command)}")
        subprocess.run(command, check=False)


if __name__ == "__main__":
    app()
