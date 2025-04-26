from datetime import datetime
from typing import Annotated
import typer


def _main(format: str) -> str:
    return datetime.now().strftime(format)


def main(
    format: Annotated[
        str, typer.Option("--format", "-f", help="Specify Datetime format.")
    ] = "%Y-%m-%d %H:%M:%S",
):
    print(f"{_main(format)}")
