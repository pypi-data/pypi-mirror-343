from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any
from zoneinfo import ZoneInfo, available_timezones

import typer


@dataclass
class Logger:
    debug_mode: bool

    def debug(self, msg: Any):
        if self.debug_mode:
            print(f"[DEBUG] {msg}")


logger = Logger(debug_mode=False)


def validate_tz(tz: str | None):
    if not tz:
        return

    if tz not in available_timezones():
        raise ValueError(f"[ERROR] タイムゾーン {tz} は不正な値です")


def _main(_tz: str | None, format: str) -> str:
    if not _tz:
        logger.debug("Since no timezone is specified, local timezone will be used.")
    tz = ZoneInfo(key=_tz) if _tz else None
    return datetime.now().astimezone(tz=tz).strftime(format)


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
    debug: Annotated[
        bool, typer.Option("--debug", "-d", help="Print debug message.")
    ] = False,
):
    if debug:
        logger.debug_mode = True
    logger.debug(f"{tz=}, {format=}")
    validate_tz(tz)
    result = _main(tz, format)
    print(f"{result}")
