from typing import Callable, Any, Dict, Optional, List


class EventObserver:
    def __init__(self) -> None:
        self._event_decorators: Dict[str, Callable[..., Any]] = {}

    def register(self, event_type: str, decorator: Callable[..., Any]) -> None:
        self._event_decorators[event_type] = decorator

    def get_registered_events(self) -> List[str]:
        return list(self._event_decorators.keys())

    def get_decorator(self, event_type: str) -> Optional[Callable[..., Any]]:
        return self._event_decorators.get(event_type)
