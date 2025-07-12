from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Any, Generic, TYPE_CHECKING, ClassVar

from ..client.context_controller import BotContextController


BaleType = TypeVar("BaleObject", bound=Any)


class BaleMethod(BotContextController, BaseModel, Generic[BaleType], ABC):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="allow",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        defer_build=True,
        json_encoders={
            bool: lambda v: 1 if v else 0
        }
    )
    
    if TYPE_CHECKING:
        __service__: ClassVar[str]
        __method__: ClassVar[str]
        
        __returning__: ClassVar[Any]
        
    else:
        @property
        @abstractmethod
        def __service__(self) -> str:
            pass
        
        @property
        @abstractmethod
        def __method__(self) -> str:
            pass
        
        @property
        @abstractmethod
        def __returning__(self) -> type:
            pass
