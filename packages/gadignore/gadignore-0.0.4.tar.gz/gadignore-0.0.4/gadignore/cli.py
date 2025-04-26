import pathlib
import shutil

import typer

app = typer.Typer()


@app.command()
def init() -> None:
    filename = ".gitignore"
    shutil.copyfile(pathlib.Path(__file__).parent / filename, pathlib.Path.cwd() / filename)


if __name__ == "__main__":
    app()
