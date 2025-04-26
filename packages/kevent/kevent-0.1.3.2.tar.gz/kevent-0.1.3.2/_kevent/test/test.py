from __future__ import annotations

from typing import Type, Callable, Generic, Union
from typeguard import typechecked
from typing_extensions import TypeVar

from kmodels.models import CoreModel
from kmodels.types import Unset, unset
from _kevent.event import Event


def b_if_unset(a: Union[T, Unset], b: T) -> T:
    if isinstance(a, Unset):
        return b
    return a


class TextEditEvent(Event):
    """Clase de pruebas que no tiene que ver con este paquete"""


class TextChangeEvent(TextEditEvent):
    """Clase de pruebas que no tiene que ver con este paquete"""


class TETextAdded(TextChangeEvent):
    """Clase de pruebas que no tiene que ver con este paquete"""
    text_added: str


class TETextRemoved(TextChangeEvent):
    n_chars: int


class EditorEvent(Event):
    """Clase de pruebas que no tiene que ver con este paquete"""
    editor_id: str


class EditorTextChangeEvent(EditorEvent):
    """Clase de pruebas que no tiene que ver con este paquete"""


class ETextAdded(EditorTextChangeEvent):
    """Clase de pruebas que no tiene que ver con este paquete"""
    position: int
    text_added: str


class ETextRemoved(EditorTextChangeEvent):
    position: int
    n_chars: int


class EditorEventConversor:
    """Clase de pruebas que no tiene que ver con este paquete"""

    def __init__(self, editor_id: str):
        self._editor_id = editor_id

    @typechecked
    def convert_text_added(self, event: TETextAdded) -> ETextAdded:
        """Convierte un TETextAdded a un ETextAdded."""
        return ETextAdded(
            editor_id=self._editor_id,  # Podrías parametrizar este ID dinámicamente
            position=event.position,
            text_added=event.text_added,
        )

    @typechecked
    def convert_text_removed(self, event: TETextRemoved) -> ETextRemoved:
        """Convierte un TETextRemoved a un ETextRemoved."""
        return ETextRemoved(
            editor_id=self._editor_id,  # Podrías parametrizar este ID dinámicamente
            position=event.position,
            n_chars=event.n_chars,
        )


EventT = TypeVar('EventT', bound=Event)

CALLBACK_T = Callable[[EventT], None]

T = TypeVar('T')


class CallActionParameters(CoreModel):
    method: Callable
    args: tuple[object, ...] | None = None
    kwargs: dict[str, object] | None = None


class EventSubscribersConfig(CoreModel):
    has_subscribers_action: CallActionParameters | Unset = unset
    lost_subscribers_action: CallActionParameters | Unset = unset

    # Has default values
    allow_multiple_subscribers: bool | Unset = unset


class EventDispatcherConfig(CoreModel):
    allow_multiple_subscribers: bool = True


class EventSubscribersConfigWrapper:
    def __init__(self, *, config: EventSubscribersConfig, dispatcher_config: EventDispatcherConfig):
        self._event = config
        self._dispatcher = dispatcher_config

    @property
    def allow_multiple_subscribers(self) -> bool:
        return b_if_unset(self._event.allow_multiple_subscribers, self._dispatcher.allow_multiple_subscribers)

    @property
    def has_subscribers_action(self) -> CallActionParameters | None:
        return self._event.has_subscribers_action

    @property
    def lost_subscribers_action(self) -> CallActionParameters | None:
        return self._event.lost_subscribers_action


class EventSubscribers(Generic[EventT]):
    __slots__ = ('_event_type', '_subscribers', '_config')

    def __init__(
            self,
            event_type: Type[CALLBACK_T],
            dispatcher_config: EventDispatcherConfig,
            event_config: EventSubscribersConfig | Unset = unset,
            subscribers: list[callable] | Unset = unset
    ):
        self._event_type = event_type
        self._config = EventSubscribersConfigWrapper(config=event_config, dispatcher_config=dispatcher_config)
        self._subscribers: list[CALLBACK_T] = subscribers if not isinstance(subscribers, Unset) else []

    @property
    def config(self) -> EventSubscribersConfigWrapper:
        return self._config

    def count(self) -> int:
        return len(self._subscribers)

    def get(self) -> list[CALLBACK_T]:
        return list(self._subscribers)

    def add(self, callback: CALLBACK_T):
        self._subscribers.append(callback)

    def get_type(self) -> Type[EventT]:
        return self._event_type.__class__

    def remove(self, callback: CALLBACK_T):
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def has_subscribers(self) -> bool:
        return len(self._subscribers) > 0

    def notify(self, event: Event):
        for callback in self._subscribers:
            callback(event)

    def __hash__(self):
        return hash(self._event_type)

    def __eq__(self, other):
        if isinstance(other, EventSubscribers):
            return self._event_type == other._event_type
        elif isinstance(other, Event):
            return self._event_type == type(other)
        return False

    def __iter__(self):
        return iter(self._subscribers)

    def __len__(self):
        return len(self._subscribers)

    def __repr__(self):
        return f"EventSubscribers(event_type={self._event_type.__name__}, subscribers_count={len(self._subscribers)})"


class EventDispatcher(Generic[EventT]):
    def __init__(
            self,
            event_map: dict[Type[EventT], EventSubscribersConfig | None],
            config: EventDispatcherConfig | None = None
    ):
        self._config = config or EventDispatcherConfig()
        self._events: dict[Type[EventT], EventSubscribers[EventT]] = {}

        self._event_map = {}
        # Iterate over event_map.items() to unpack both the event and its configuration
        for event, event_config in event_map.items():
            self._event_map[event] = event_config or EventSubscribersConfig()

        # Prepare the event subscribers
        for event, event_config in self._event_map.items():
            event_subscribers = EventSubscribers[EventT](
                event_type=event,
                dispatcher_config=self._config,
                event_config=event_config
            )

            self._events[event] = event_subscribers

    def subscribe(self, event_type: Type[EventT], callback: CALLBACK_T):
        es = self._events[event_type]
        has_subscribers = es.has_subscribers()
        es.add(callback)

        # Funcionalidad para ejecutar una acción cuando empiezan a haber suscriptores
        has_subscribers_action = es.config.has_subscribers_action
        if has_subscribers_action and not has_subscribers:
            method = has_subscribers_action.method
            args = has_subscribers_action.args or ()
            kwargs = has_subscribers_action.kwargs or {}
            method(*args, **kwargs)

    def unsubscribe(self, event_type: Type[EventT], callback: CALLBACK_T):
        es = self._events[event_type]
        has_subscribers = es.has_subscribers()
        es.remove(callback)

        # Funcionalidad para ejecutar una acción cuando se pierden los suscriptores
        lost_subscribers_action = es.config.lost_subscribers_action
        if lost_subscribers_action and has_subscribers and not es.has_subscribers():
            method = lost_subscribers_action.method
            args = lost_subscribers_action.args or ()
            kwargs = lost_subscribers_action.kwargs or {}
            method(*args, **kwargs)

    def has_subscribers(self, event_type: Type[EventT]) -> bool:
        return event_type in self._events and len(self._events[event_type]) > 0

    def dispatch(self, event: Event):
        event_type = type(event)
        if event_type not in self._events:
            return

        self._events[event_type].notify(event)

    def __repr__(self):
        events_info = ", ".join(
            f"{sub._event_type.__name__}: {sub.count()} subscriber(s)"
            for sub in self._events.values()  # Iterate over the values, not the keys
        )
        return f"EventDispatcher(events=[{events_info}])"


class TextEdit:
    """Clase de pruebas que no tiene que ver con este paquete"""

    def __init__(self):
        self._text_edit_connected: bool = False

        event_map = {
            TETextAdded: EventSubscribersConfig(
                has_subscribers_action=CallActionParameters(
                    method=self.connect_text_added,
                    args=('123',)
                ),
                lost_subscribers_action=CallActionParameters(
                    method=self.disconnect_text_added,
                    args=('123',),
                    kwargs={'other_password': '456'}
                )
            ),
        }
        self._dispatcher: EventDispatcher[TextEditEvent] = EventDispatcher(event_map)

        self._text = ""

    @property
    def dispatcher(self) -> EventDispatcher[TextEditEvent]:
        return self._dispatcher

    def write(self, text: str):
        self._text = text

        if self._text_edit_connected:
            self._on_text_changed(text)

    def remove(self, n_chars: int):
        if not n_chars:
            return
        if n_chars > len(self._text):
            n_chars = len(self._text)

        _n_chars = len(self._text) if n_chars > len(self._text) else n_chars

        # if self._text_edit_connected:
        #     self._on_text_changed(text)

    def _on_text_changed(self, n_chars: int):
        if n_chars > 0:
            event = TETextAdded(text_added=self._text[-n_chars:])
        elif n_chars < 0:
            event = TETextRemoved(n_chars=n_chars)
        else:
            raise ValueError("Unexpected behavior")

        print(f'EVENTO GENERADO PERO NO ENVIADO TODAVÍA: {repr(event)}')

    def connect_text_added(self, password: str = "whatever"):
        if password != '123':
            print('CONNECT NOT ALLOWED')
            return False
        print('CONNECT ALLOWED')
        self._text_edit_connected = True

    def disconnect_text_added(self, password: str = "whatever", other_password: str = "whatever"):
        if password != '123' and other_password != '456':
            print('DISCONNECT NOT ALLOWED')
            return False
        print('DISCONNECT ALLOWED')
        self._text_edit_connected = False


class Editor:
    """Clase de pruebas que no tiene que ver con este paquete"""

    def __init__(self):
        pass


def test():
    text_edit = TextEdit()

    # Caso 1: Sin suscriptores, no debería generar eventos
    print("Caso 1: Sin suscriptores")
    text_edit.write("Texto sin suscriptores")  # No debería generar eventos

    # Caso 2: Conectar un suscriptor y generar un evento
    print("\nCaso 2: Con suscriptores")
    callback = lambda event: print(f"Evento recibido: {event.text_added}")
    text_edit.dispatcher.subscribe(TETextAdded, callback)
    text_edit.write("Texto con suscriptores")  # Debería generar eventos

    # Caso 3: Desconectar el suscriptor y verificar que no se generan eventos
    print("\nCaso 3: Sin suscriptores después de desconectar")
    text_edit.dispatcher.unsubscribe(TETextAdded, callback)
    text_edit.write("Texto después de desconectar")  # No debería generar eventos


test()
