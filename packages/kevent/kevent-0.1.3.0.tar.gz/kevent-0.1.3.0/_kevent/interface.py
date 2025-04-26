from abc import abstractmethod, ABC
from collections import defaultdict
from typing import Generic, DefaultDict, Callable, Type, Set, Iterable
from queue import Queue

from kmodels.types import Unset, unset
from _kevent.event import EVENT_T

from typeguard import typechecked

"""
Cosas que mejorar
- Añadir un método para habilitar/deshabilitar el despacho de eventos.
- Añadir un método para limpiar la lista de eventos.
- Añadir un método para limpiar la lista de eventos de ciertos tipos en específico.

- Crear/usar una clase queue apropiada para evitar que se acceda simultáneamente a la lista de eventos en lugar de usar
  una lista normal.

- Crear un bloqueador más robusto que tenga en cuenta tanto la petición del usuario de bloqueo como el autobloqueo.
  Es decir, que cuando EventDispatcher se bloquee por sí mismo, pero también por parte del usuario, que al terminar el
  bloqueo autoimpuesto no se desbloquee si el usuario tampoco ha quitado su bloqueo.

"""
EVENT_OR_EVENTS_T = EVENT_T | Iterable[EVENT_T]


@typechecked
def to_event_tuple(event_or_events: EVENT_OR_EVENTS_T) -> tuple[EVENT_T, ...]:
    """
    Convierte un único evento o una colección de eventos en una tupla de eventos.
    """
    if event_or_events is unset or event_or_events is None:
        return tuple()

    if isinstance(event_or_events, Iterable):
        return tuple(event_or_events)

    return (event_or_events,)


class EventDispatcherInterface(Generic[EVENT_T], ABC):
    @abstractmethod
    def has_subscribers(self, event_type: Type[EVENT_T]) -> bool:
        ...

    @abstractmethod
    def subscribe(self, event_type: Type[EVENT_T], callback: Callable[[EVENT_T], None]):
        ...

    @abstractmethod
    def unsubscribe(self, event_type: Type[EVENT_T], callback: Callable[[EVENT_T], None]):
        ...

    @abstractmethod
    def add_events_to_queue(self, event_or_events: EVENT_OR_EVENTS_T):
        ...

    @abstractmethod
    def dispatch(self, event_or_events: EVENT_OR_EVENTS_T | Unset | None = unset):
        ...
