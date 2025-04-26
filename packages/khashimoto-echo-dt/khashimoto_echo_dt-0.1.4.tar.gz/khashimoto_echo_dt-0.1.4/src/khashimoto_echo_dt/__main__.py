import typer
from .main import main as _main


def main():
    typer.run(_main)


main()
