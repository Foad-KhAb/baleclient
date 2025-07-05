from typing import Any


class IntBool:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            if v in (0, 1):
                return bool(v)
        raise ValueError("Must be 0 or 1 or boolean")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="integer", enum=[0, 1])

    def __repr__(self):
        return "IntBool"

    def __str__(self):
        return "IntBool"
