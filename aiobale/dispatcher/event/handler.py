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
    """
    A class that represents an event handler with associated filters and a callback.
    
    Attributes:
        event_type (str): The type of event this handler is associated with.
        callback (Callable[..., Union[Coroutine[Any, Any, Any], Any]]): 
            The function to be called when the event is triggered. 
            It can be a coroutine or a regular function.
        filters (List[Callable[..., Union[bool, Awaitable[bool]]]]): 
            A list of filter functions that determine whether the handler should be executed. 
            Each filter can be synchronous or asynchronous.
            
    Methods:
        async check(*args: Any, **kwargs: Any) -> bool:
            Evaluates all filters with the provided arguments. 
            Returns True if all filters pass, otherwise False.
        async call(*args: Any, **kwargs: Any) -> Any:
            Executes the callback function with the provided arguments. 
            If the callback is a coroutine, it is awaited; otherwise, it is executed in a thread pool.
    """
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
