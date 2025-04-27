from typing import Any
from typing import ClassVar
from typing import Self
from typing import TypeVar

import pydantic
from pydantic_core import CoreSchema
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from pydantic import GetJsonSchemaHandler


T = TypeVar('T')


class HTTPHeaderType:
    __module__: str = 'libcanonical.types'
    openapi_title: ClassVar[str | None] = None
    openapi_description: ClassVar[str | None] = None
    max_length: int | None = None
    min_length: int | None = None

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=cls.__default_schema__(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.chain_schema([
                    cls.__default_schema__(),
                    core_schema.no_info_plain_validator_function(cls.transform),
                    core_schema.no_info_plain_validator_function(cls.validate),
                    core_schema.no_info_plain_validator_function(cls)
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
        schema['title'] = cls.openapi_title or cls.__name__
        if cls.openapi_title is not None:
            schema['description'] = cls.openapi_title
        return schema

    @classmethod
    def __default_schema__(cls):
        return core_schema.str_schema(
            max_length=cls.max_length,
            min_length=cls.min_length,
        )

    @classmethod
    def transform(cls, v: str) -> str:
        return v

    @classmethod
    def parse(cls, value: str) -> Self:
        adapter: pydantic.TypeAdapter[Any] = pydantic.TypeAdapter(cls)
        return adapter.validate_python(value)

    @classmethod
    def validate(cls, v: str) -> str:
        return v

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str: # pragma: no cover
        return f'<{type(self).__name__}: {str(self)}>'