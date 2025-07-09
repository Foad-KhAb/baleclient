from pydantic import BaseModel, ConfigDict

from ..client.context_controller import BotContextController


class BaleObject(BotContextController, BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="allow",
        frozen=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        defer_build=True,
        json_encoders={
            bool: lambda v: 1 if v else 0
        }
    )
