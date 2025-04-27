import asyncio
import datetime
import logging
import email.utils
from typing import TypeVar

from pydantic_core import core_schema

from .httpheadertype import HTTPHeaderType


T = TypeVar('T')

INVALID = object()


class HTTPRetryAfter(HTTPHeaderType):
    __module__: str = 'libcanonical.types'
    default_delay: float = 5.0
    nbf: datetime.datetime
    logger: logging.Logger = logging.getLogger(__name__)

    @property
    def seconds(self):
        return int((self.nbf - self.now).total_seconds())

    @classmethod
    def __default_schema__(cls):
        return core_schema.union_schema([
            core_schema.chain_schema([
                core_schema.no_info_plain_validator_function(email.utils.parsedate_to_datetime),
                core_schema.no_info_plain_validator_function(
                    lambda x: (
                        datetime.datetime.astimezone(x, datetime.timezone.utc)
                    )
                )
            ]),
            core_schema.chain_schema([
                core_schema.int_schema(ge=0),
                core_schema.no_info_plain_validator_function(lambda x: (
                    datetime.datetime.now(datetime.timezone.utc)
                    + datetime.timedelta(seconds=x)
                ))
            ]),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(
                    lambda x: cls.logger.warning('Invalid Retry-After value: %s', str(x)[:32])
                ),
                core_schema.no_info_plain_validator_function(lambda x: INVALID)
            ]),
            core_schema.none_schema(),
        ])

    def __init__(self, nbf: datetime.datetime | None):
        self.now = datetime.datetime.now(datetime.timezone.utc)
        if nbf == INVALID:
            nbf = self.now + datetime.timedelta(seconds=5)
        self.nbf = nbf or self.now
        assert isinstance(self.nbf, datetime.datetime)

    def delay(
        self,
        default: float | None = None,
        max_delay: float | None = None
    ):
        num_seconds = max(default or self.seconds, self.seconds)
        return asyncio.sleep(min(num_seconds, max_delay or num_seconds))

    def __str__(self): # pragma: no cover
        return str(self.nbf)