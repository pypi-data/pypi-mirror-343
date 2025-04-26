from collections import defaultdict
from typing import Generic, DefaultDict, Callable, Type, Set

from kmodels.types import Unset, unset
from _kevent.event import EVENT_T
from typeguard import typechecked

from klocker.simple import SimpleLocker


class EventDispatcher(Generic[EVENT_T]):
    @typechecked
    def __init__(
            self,
            *,
            whitelist: Set[Type[EVENT_T]] | Unset = unset,
            blacklist: Set[Type[EVENT_T]] | Unset = unset,
            allow_multiple: bool = False
    ):
        # Tipo de evento -> lista de callbacks
        self._listeners: DefaultDict[Type[EVENT_T], list[Callable[[EVENT_T], None]]] = defaultdict(list)
        self._whitelist: Set[Type[EVENT_T]] | Unset = whitelist
        self._blacklist: Set[Type[EVENT_T]] | Unset = blacklist
        self._allow_multiple: bool = allow_multiple

    def _validate_event_type(self, event_type: Type[EVENT_T]):
        """Valida el tipo de evento contra la whitelist y blacklist."""
        if self._whitelist is not unset and event_type not in self._whitelist:
            raise ValueError(f"El tipo de evento {event_type.__name__} no está en la whitelist.")
        if self._blacklist is not unset and event_type in self._blacklist:
            raise ValueError(f"El tipo de evento {event_type.__name__} está en la blacklist.")

    @typechecked
    def has_subscribers(self, event_type: Type[EVENT_T]) -> bool:
        """Verifica si hay suscriptores exactamente para el tipo dado."""
        return event_type in self._listeners and len(self._listeners[event_type]) > 0

    @typechecked
    def subscribe(self, event_type: Type[EVENT_T], callback: Callable[[EVENT_T], None]):
        """Registra un callback para un tipo de evento."""
        self._validate_event_type(event_type)
        if not self._allow_multiple and event_type in self._listeners and callback in self._listeners[event_type]:
            raise ValueError(f"El callback ya está registrado para el tipo de evento {event_type.__name__}.")
        self._listeners[event_type].append(callback)

    @typechecked
    def unsubscribe(self, event_type: Type[EVENT_T], callback: Callable[[EVENT_T], None]):
        """Elimina un callback registrado para un tipo de evento."""
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
            if not self._listeners[event_type]:
                del self._listeners[event_type]

    @typechecked
    def dispatch(self, event: EVENT_T):
        """Lanza el evento a los callbacks registrados para su tipo exacto."""
        event_type = type(event)
        self._validate_event_type(event_type)
        for callback in self._listeners.get(event_type, []):
            callback(event)

    def __repr__(self):
        listeners_repr = ",\n".join(
            f"  {event_type.__name__}: {len(callbacks)} subscriber(s)"
            for event_type, callbacks in self._listeners.items()
        )
        return f"EventDispatcher(\n{listeners_repr}\n)"
