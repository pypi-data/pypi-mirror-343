from __future__ import annotations

from typing import Generic, Type, Callable

from typeguard import typechecked

from kevent.dispatcher.simple.callback import SimpleEventCallback
from kevent.dispatcher.simple.constants import CALLABLE_T
from kevent.dispatcher.simple.dispatcher.config import SimpleEventDispatcherConfigInterface
from kevent.dispatcher.types import CALLBACK_T
from kevent.event import EVENT_T, Event


def to_callback(callback: CALLBACK_T) -> SimpleEventCallback:
    if isinstance(callback, SimpleEventCallback):
        return callback
    elif isinstance(callback, Callable):
        return SimpleEventCallback(callback)
    else:
        raise TypeError(f"Callback debe ser una función o una instancia de Callback, no {type(callback)}")


class SimpleEventSubscribers(Generic[EVENT_T]):
    def __init__(self, config_interface: SimpleEventDispatcherConfigInterface, event_type: Type[EVENT_T]):
        self._event_type = event_type
        self._config = config_interface
        self._subscribers: dict[SimpleEventCallback[EVENT_T], SimpleEventCallback[EVENT_T]] = {}

    def has_subscribers(self) -> bool:
        return len(self) > 0

    @typechecked
    def subscribe(self, callback: SimpleEventCallback[EVENT_T] | CALLABLE_T):
        self._raise_multiple_subscribers(callback)

        _callback = to_callback(callback)
        if _callback in self._subscribers:
            self._subscribers[_callback].increase()
        else:
            self._subscribers[_callback] = _callback

    @typechecked
    def unsubscribe(self, callback: CALLABLE_T, *, from_all: bool = False):
        if callback not in self._subscribers:
            raise KeyError(f'El callback {callback} no está registrado')

        _callback = to_callback(callback)
        if from_all:
            del self._subscribers[_callback]
        else:
            try:
                self._subscribers[_callback].decrease()
            except ValueError:
                del self._subscribers[_callback]

    @typechecked
    def dispatch(self, event: EVENT_T):
        for callback in self._subscribers.values():
            callback(event)

    def __eq__(self, other):
        if isinstance(other, SimpleEventSubscribers):
            return self._event_type == other._event_type
        elif isinstance(other, Event):
            return self._event_type == type(other)
        else:
            return False

    def __hash__(self):
        return hash(self._event_type)

    def __len__(self) -> int:
        return sum(len(s) for s in self._subscribers.values())

    def __repr__(self):
        return f"EventSubscribers(event_type={self._event_type.__name__}, subscribers_count={len(self)})"

    @typechecked
    def _raise_multiple_subscribers(self, callback: CALLABLE_T):
        if self._config.allow_multiple:
            return
        callback_id = id(callback)
        if callback_id in self._subscribers:
            raise ValueError(
                f'Ya has suscrito una vez el callback {callback} para el evento {self._event_type.__name__}.'
            )
