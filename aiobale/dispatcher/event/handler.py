import asyncio
import inspect
from dataclasses import dataclass, field
from typing import (
    Callable,
    Coroutine,
    Union,
    Awaitable,
    Any,
    List,
    TypeVar
)

T_Event = TypeVar("T_Event")
T_Result = TypeVar("T_Result")


@dataclass
class Handler:
    event_type: str
    callback: Callable[..., Union[Coroutine[Any, Any, Any], Any]]
    filters: List[Callable[..., Union[bool, Awaitable[bool]]]] = field(default_factory=list)

    async def check(self, *args: Any, **kwargs: Any) -> bool:
        for filter_func in self.filters:
            result = filter_func(*args, **kwargs)
            if inspect.isawaitable(result):
                result = await result
            else:
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(None, lambda: result)

            if not result:
                return False
        return True

    async def call(self, *args: Any, **kwargs: Any) -> Any:
        if inspect.iscoroutinefunction(self.callback):
            return await self.callback(*args, **kwargs)
        else:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.callback(*args, **kwargs))
