import pydantic
import pytest

from libcanonical.types import HTTPRetryAfter


@pytest.mark.parametrize("value", [
    "2",
    "Wed, 23 Sep 2009 22:15:29 GMT"
])
def test_valid_values(value: str):
    HTTPRetryAfter.parse(value)


@pytest.mark.parametrize("value", [
    "a",
])
def test_invalid_values(value: str):
    header = HTTPRetryAfter.parse(value)
    assert header.seconds == HTTPRetryAfter.default_delay


@pytest.mark.parametrize("value", [
    None,
])
def test_none(value: str):
    header = HTTPRetryAfter.parse(value)
    assert header.seconds == 0.0