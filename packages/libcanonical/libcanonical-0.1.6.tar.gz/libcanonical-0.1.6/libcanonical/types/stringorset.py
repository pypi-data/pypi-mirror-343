from typing import Any
from collections import abc

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core import core_schema


class StringOrSet(set[str]):
    __module__: str = 'libcanonical.types'

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.union_schema([
                core_schema.str_schema(),
                core_schema.list_schema(),
            ]),
            python_schema=core_schema.union_schema([
                core_schema.chain_schema([
                    core_schema.is_instance_schema(str),
                    core_schema.no_info_plain_validator_function(cls.fromstring)
                ]),
                core_schema.chain_schema([
                    core_schema.is_instance_schema(abc.Collection),
                    core_schema.no_info_plain_validator_function(cls)
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(list)
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.union_schema([
            core_schema.str_schema(),
            core_schema.list_schema()
        ]))

    @classmethod
    def fromstring(cls, v: str):
        return cls({v})