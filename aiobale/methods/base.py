from pydantic import BaseModel, ConfigDict


class BaleMethod(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="allow",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        defer_build=True
    )
