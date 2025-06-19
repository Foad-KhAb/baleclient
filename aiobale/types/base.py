from pydantic import BaseModel, ConfigDict

class BaleObject(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="allow",
        frozen=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        defer_build=True
    )
