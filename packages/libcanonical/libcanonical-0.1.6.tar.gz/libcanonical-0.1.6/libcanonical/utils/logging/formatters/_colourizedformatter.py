from __future__ import annotations
import collections.abc
import datetime
import json
import logging
import sys
from copy import copy
from typing import Callable
from typing import Literal

import click
import pydantic

TRACE_LOG_LEVEL = 5


def format_colors(color: str) -> Callable[[str], str]:
    return lambda level_name: click.style(level_name, fg=color)


class ColourizedFormatter(logging.Formatter):
    """A custom log formatter class that:

    * Outputs the LOG_LEVEL with an appropriate color.
    * If a log call includes an `extra={"color_message": ...}` it will be used
      for formatting the output, instead of the plain text message.
    """
    __module__: str = 'libcanonical.utils.logging'

    level_name_colors: dict[int, Callable[..., str]] = {
        TRACE_LOG_LEVEL: format_colors("blue"),
        logging.DEBUG: format_colors("cyan"),
        logging.INFO: format_colors("green"),
        logging.WARNING: format_colors("yellow"),
        logging.ERROR: format_colors("red"),
        logging.CRITICAL: format_colors("bright_red"),
    }

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        use_colors: bool | None = None,
    ):
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_level_name(self, level_name: str, level_no: int) -> str:
        def default(level_name: str) -> str:
            return str(level_name)  # pragma: no cover

        func = self.level_name_colors.get(level_no, default)
        return func(level_name)

    def should_use_colors(self) -> bool:
        return True  # pragma: no cover

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None):
        if not datefmt:
            return super().formatTime(record, datefmt=datefmt)

        return datetime.datetime.fromtimestamp(record.created).astimezone().strftime(datefmt)

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        seperator = " " * (8 - len(recordcopy.levelname))
        message = recordcopy.getMessage()
        if isinstance(message, pydantic.BaseModel):
            message = message.model_dump(mode='json')
        if isinstance(message, collections.abc.Mapping):
            if message.get('message'):
                message = message['message']
            else:
                message = json.dumps(message, indent=2)

        if self.use_colors:
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            if "color_message" in recordcopy.__dict__:
                recordcopy.msg = recordcopy.__dict__["color_message"]
                recordcopy.__dict__["message"] = message
        recordcopy.__dict__["levelprefix"] = levelname + ":" + seperator
        return super().formatMessage(recordcopy)