from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Callable, Coroutine
from typing import Any

EventHandler = Callable[[Any], Coroutine[Any, Any, None]]


class IEventBus(ABC):
    @abstractmethod
    async def publish(self, event: Any) -> None: ...

    @abstractmethod
    def subscribe(self, event_type: type, handler: EventHandler) -> None: ...


class InMemoryEventBus(IEventBus):
    def __init__(self) -> None:
        self._handlers: dict[type, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: Any) -> None:
        for handler in self._handlers[type(event)]:
            await handler(event)
