from typing import Any
from pydantic import GetCoreSchemaHandler
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import core_schema


class IntBool:
    @classmethod
    def validate(cls, v: Any) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            if v in (0, 1):
                return bool(v)
        raise ValueError("Must be 0 or 1 or boolean")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler):
        json_schema = handler(schema)
        json_schema.update(type="integer", enum=[0, 1])
        return json_schema

    def __repr__(self):
        return "IntBool"

    def __str__(self):
        return "IntBool"
