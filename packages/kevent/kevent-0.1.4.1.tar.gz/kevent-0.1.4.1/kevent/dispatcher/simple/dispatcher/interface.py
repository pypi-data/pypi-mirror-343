from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Type, Iterable, Tuple

from kevent.dispatcher.simple.constants import CALLABLE_T
from kevent.event import EVENT_T


class SimpleEventDispatcherInterface(Generic[EVENT_T], ABC):
    @property
    @abstractmethod
    def config(self): ...

    @abstractmethod
    def is_enabled(self) -> bool: ...

    @abstractmethod
    def enable(self, enable: bool = True): ...

    @abstractmethod
    def clear_queue(self): ...

    @abstractmethod
    def has_subscribers(self, event_type: Type[EVENT_T]) -> bool: ...

    @abstractmethod
    def is_subscribed(self, event_type: Type[EVENT_T], callback: CALLABLE_T) -> bool: ...

    @abstractmethod
    def subscribe(self, event_type: Type[EVENT_T], callback: CALLABLE_T): ...

    @abstractmethod
    def unsubscribe(self, event_type: Type[EVENT_T], callback: CALLABLE_T, *, from_all: bool = True): ...

    @abstractmethod
    def dispatch(self, events: Iterable[EVENT_T] | tuple[EVENT_T, ...] | EVENT_T): ...