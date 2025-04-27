from typing import Generic, Callable

from kevent.dispatcher.simple.constants import CALLABLE_T
from kevent.event import EVENT_T


class SimpleEventCallback(Generic[EVENT_T]):
    def __init__(self, func: CALLABLE_T):
        self._func = func
        self._n_subscribers = 1

    def __call__(self, event: EVENT_T):
        for _ in range(self._n_subscribers):
            self._func(event)

    def increase(self):
        self.set(self._n_subscribers + 1)

    def decrease(self):
        self.set(self._n_subscribers - 1)

    def set(self, n_subscribers: int):
        self._n_subscribers = n_subscribers
        if n_subscribers < 0:
            raise ValueError("n_subscribers must be non-negative")

    def __len__(self) -> int:
        return self._n_subscribers

    @property
    def id(self) -> int:
        return id(self._func)

    def __hash__(self):
        return hash(self._func)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SimpleEventCallback):
            return self.id == other.id
        elif isinstance(other, Callable):
            return self.id == id(other)
        else:
            raise TypeError(f"Cannot compare Callback with {type(other)}")
