from datetime import datetime
from typing import Annotated, Any
from zoneinfo import ZoneInfo
import typer


def debug_log(debug: bool, msg: Any):
    if debug:
        print(f"[DEBUG] {msg}")


def _main(tz: str | None, format: str) -> str:
    tz = ZoneInfo(key=tz) if tz else None
    return datetime.now(tz=tz).strftime(format)


def main(
    tz: Annotated[
        str | None,
        typer.Argument(
            help="Specify timezone e.g. 'Asia/Tokyo'. If not specified, local timezone will be used."
        ),
    ] = None,
    format: Annotated[
        str, typer.Option("--format", "-f", help="Specify Datetime format.")
    ] = "%Y-%m-%d %H:%M:%S",
    debug: Annotated[bool, typer.Option(help="Print debug message.")] = False,
):
    debug_log(debug, f"{tz=}, {format=}")
    result = _main(tz, format)
    print(f"{result}")
