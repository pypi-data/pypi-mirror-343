import re
from typing import Any
from typing import Self
from typing_extensions import SupportsIndex

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core import core_schema


class DomainName(str):
    __module__: str = 'libcanonical.types'
    pattern: re.Pattern[str] = re.compile(r'^([0-9a-z\-_]+)$')
    min_length: int = 3
    max_length: int = 255

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=cls.__default_schema__(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.chain_schema([
                    cls.__default_schema__(),
                    core_schema.no_info_plain_validator_function(cls.validate)
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        schema = handler(cls.__default_schema__())
        schema['title'] = 'DomainName'
        schema['description'] = (
            "An RFC domain name follows the specifications set by RFC 1035 "
            "and related standards, defining a structured, hierarchical naming "
            "system used in the Domain Name System (DNS), consisting of labels "
            "separated by dots (e.g., `example.com`), with rules for length, "
            "character usage, and resolution to IP addresses."
        )
        return schema

    @classmethod
    def __default_schema__(cls):
        return core_schema.str_schema(
            min_length=cls.min_length,
            max_length=cls.max_length
        )

    @classmethod
    def validate(cls, v: Any, _: Any = None) -> Self:
        if not isinstance(v, str):
            raise ValueError(f"Can not create DomainName from {type(v).__name__}")
        if not v:
            raise ValueError("A domain name can not be an empty string.")
        if len(v) > 253:
            raise ValueError("Value is too long to be a valid domain name.")
        v = str.lower(v)
        labels: list[str] = str.split(v, '.')
        for label in labels:
            if label.startswith('-') or label.endswith('-'):
                raise ValueError("A DNS label can not start or end with a hyphen.")
            if not cls.pattern.match(label):
                raise ValueError("Invalid characters in DNS label.")
            if len(label) > 63:
                raise ValueError("A DNS label is at most 63 characters.")
        return cls(v)

    def __getitem__(self, __i: SupportsIndex | slice) -> str:
        value = str.split(self, '.')[__i]
        if isinstance(value, list):
            value = str.join('.', value)
        return value