from collections import defaultdict
from typing import Any, Awaitable, Callable, Coroutine, Dict, List, Optional, Union, Type

from .event.handler import Handler
from .event.observer import EventObserver


class Router:
    def __init__(self, name: Optional[str] = None) -> None:
        self.name: str = name or hex(id(self))
        self._handlers: Dict[str, List[Handler]] = defaultdict(list)
        self._observer = EventObserver()

        self._register_default_event_types()
        
        self.message = self._observer.get_decorator("message")
        self.message_deleted = self._observer.get_decorator("message_deleted")
        self.chat_deleted = self._observer.get_decorator("chat_deleted")
        self.chat_cleared = self._observer.get_decorator("chat_cleared")
        self.username_changed = self._observer.get_decorator("username_changed")
        self.message_sent = self._observer.get_decorator("message_sent")
        self.message_edited = self._observer.get_decorator("message_edited")

    def _register_default_event_types(self) -> None:
        for event_type in (
            "message", 
            "message_deleted",
            "chat_cleared",
            "chat_deleted",
            "username_changed",
            "message_sent",
            "message_edited"
        ):
            self._observer.register(event_type, self._make_event_decorator(event_type))

    def _make_event_decorator(self, event_type: str) -> Callable[..., Callable[..., Coroutine[Any, Any, Any]]]:
        def decorator(*filters: Callable[..., Union[bool, Awaitable[bool]]]):
            return self.register(event_type, *filters)
        return decorator

    def add_event_type(self, event_type: str) -> None:
        self._observer.register(event_type, self._make_event_decorator(event_type))

    def register(
        self,
        event_type: str,
        *filters: Callable[..., Union[bool, Awaitable[bool]]],
    ) -> Callable[[Callable[..., Coroutine[Any, Any, Any]]], Callable[..., Coroutine[Any, Any, Any]]]:

        def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
            handler = Handler(event_type=event_type, callback=func, filters=list(filters))
            self._handlers[event_type].append(handler)
            return func

        return decorator

    def get_handlers(self, event_type: str) -> List[Handler]:
        return self._handlers.get(event_type, [])

    def available_event_types(self) -> List[str]:
        return list(self._handlers.keys())

    def all_handlers(self) -> Dict[str, List[Handler]]:
        return self._handlers

    def handler_count(self) -> int:
        return sum(len(handlers) for handlers in self._handlers.values())
