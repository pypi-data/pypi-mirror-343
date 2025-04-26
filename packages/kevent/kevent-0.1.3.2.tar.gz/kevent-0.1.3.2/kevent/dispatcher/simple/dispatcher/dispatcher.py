from __future__ import annotations

from collections import defaultdict

from klocker.simple import SimpleLocker
from klocker.simple.locker.config import SimpleLockerConfig
from klocker.simple.thread.state import SimpleThreadLockFailure, SimpleThreadExecutionFailure
from klocker.simple.user import SimpleLockerUserInterface
from typeguard import typechecked
from typing import Generic, DefaultDict, Type, Iterable, Tuple

from kevent.event import EVENT_T, Event
from kmodels.types import Unset, unset
from kevent.dispatcher.simple.constants import CALLABLE_T
from kevent.dispatcher.simple.dispatcher.config import (
    SimpleEventDispatcherConfigHandler, SimpleEventDispatcherConfigInterface, SimpleEventDispatcherConfig
)
from kevent.dispatcher.simple.subscribers import SimpleEventSubscribers


@typechecked
def to_event_list(events: Iterable[EVENT_T] | Tuple[EVENT_T] | EVENT_T | Unset | None) -> list[EVENT_T]:
    if events is None or isinstance(events, Unset):
        events = list()
    elif isinstance(events, list):
        ...
    elif isinstance(events, tuple):
        events = [e for e in events]
    elif isinstance(events, Event):
        events = [events]
    elif isinstance(events, Iterable):
        events = list(events)
    else:
        events = list()

    return events


class SimpleEventDispatcher(Generic[EVENT_T]):
    @typechecked
    def __init__(
            self,
            event_types: list[Type[EVENT_T]],
            *,
            config: SimpleEventDispatcherConfig | Unset = unset,
    ):
        self._config = SimpleEventDispatcherConfigHandler(config)

        self._subscribers: dict[EVENT_T, SimpleEventSubscribers[EVENT_T]] = {}
        for event in event_types:
            self._subscribers[event] = SimpleEventSubscribers(self.config, event)

        self._listeners: DefaultDict[Type[EVENT_T], list[CALLABLE_T]] = defaultdict(list)

        self._on = True
        self._event_queue: list[EVENT_T] = []
        locker_config = SimpleLockerConfig(on_locked='wait', timeout=None, max_waiters=1)
        self._locker: SimpleLocker = SimpleLocker(config=locker_config)

    @property
    def config(self) -> SimpleEventDispatcherConfigInterface:
        return self._config.interface

    def is_enabled(self) -> bool:
        return self._on

    def enable(self, enable: bool = True):
        self._on = enable

    def clear_queue(self):
        self._locker.with_locker(self._clear_func)

    @typechecked
    def has_subscribers(self, event_type: Type[EVENT_T]) -> bool:
        self._raise_unknown_event_type(event_type)
        return self._subscribers[event_type].has_subscribers()

    @typechecked
    def subscribe(self, event_type: Type[EVENT_T], callback: CALLABLE_T):
        self._raise_unknown_event_type(event_type)
        self._subscribers[event_type].subscribe(callback)

    @typechecked
    def unsubscribe(self, event_type: Type[EVENT_T], callback: CALLABLE_T, *, from_all: bool = True):
        self._raise_unknown_event_type(event_type)
        self._subscribers[event_type].unsubscribe(callback, from_all=from_all)

    @typechecked
    def dispatch(self, events: Iterable[EVENT_T] | Tuple[EVENT_T] | EVENT_T | Unset = unset):
        _events = self._to_event_list(events)

        self._append_events(_events)
        if self._on:
            self._locker.with_locker(self._dispatch_func, self._dispatch_callback)

    def __repr__(self) -> str:
        subscribers_repr = ", ".join(
            f"{event_type.__name__}: {len(subscribers)} subscriber(s)"
            for event_type, subscribers in self._subscribers.items()
        )
        return f"EventDispatcher(subscribers={{ {subscribers_repr} }})"

    def _clear_func(self):
        self._event_queue.clear()

    def _dispatch_func(self, ui: SimpleLockerUserInterface):
        """
        Safely processes events in the queue one by one, ensuring no concurrent modification issues.
        """
        while self._event_queue:
            # Check if the dispatcher is still enabled
            if not self.is_enabled():
                break

            # Remove the first event from the queue and process it
            ev = self._event_queue.pop(0)
            self._subscribers[type(ev)].dispatch(ev)

    @classmethod
    def _dispatch_callback(cls, ui: SimpleLockerUserInterface):
        """
        Función invocada en caso de que ocurra algún problema con _dispatch_func.
        Es posible que la quitemos en un futuro, pero
        """
        if isinstance(ui.thread.state.failure_details, SimpleThreadLockFailure):
            return

        t_id = ui.thread.name
        m = 'An unexpected error occurred while dispatching the event. Details:\n'
        if isinstance(ui.thread.state.failure_details, SimpleThreadExecutionFailure):
            m += f'\tThread-{t_id} was interrupted in the middle of its execution. Details:\n'
        else:
            m += f"\tUnknown error. Details: \n"
        m += f"{repr(ui.thread.state.failure_details)}.\n"
        print(m)

    def _append_events(self, events: list[EVENT_T]):
        self._event_queue.extend(events)

    def _to_event_list(self, events: Iterable[EVENT_T]) -> list[EVENT_T]:
        _events = to_event_list(events)
        for ev in _events:
            ev_type = type(ev)
            if ev_type not in self._subscribers:
                e_name = ev_type.__name__
                raise TypeError(f'El evento `{e_name}` no esta programado para ser utilizado por este dispatcher.')
        return _events

    def _raise_unknown_event_type(self, event_type: Type[EVENT_T]):
        if event_type not in self._subscribers:
            e_name = event_type.__name__
            raise TypeError(f'El evento `{e_name}` no esta programado para ser utilizado por este dispatcher.')
