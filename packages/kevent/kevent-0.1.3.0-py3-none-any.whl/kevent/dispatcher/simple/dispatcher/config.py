from __future__ import annotations

from abc import abstractmethod, ABC

from kmodels.models import CoreModel
from kmodels.types import Unset, unset


class SimpleEventDispatcherConfig(CoreModel):
    allow_multiple: bool = False


class SimpleBaseEventDispatcherConfigHandler(ABC):
    def __init__(self, config: SimpleEventDispatcherConfig | Unset = unset):
        self._config = config if not isinstance(config, Unset) else SimpleEventDispatcherConfig()

    @property
    @abstractmethod
    def allow_multiple(self) -> bool:
        ...


class SimpleEventDispatcherConfigInterface(SimpleBaseEventDispatcherConfigHandler):
    @property
    def allow_multiple(self) -> bool:
        return self._config.allow_multiple


class SimpleEventDispatcherConfigController(SimpleBaseEventDispatcherConfigHandler):
    @property
    def allow_multiple(self) -> bool:
        return self._config.allow_multiple


class SimpleEventDispatcherConfigHandler:
    def __init__(self, config: SimpleEventDispatcherConfig):
        self._interface = SimpleEventDispatcherConfigInterface(config)
        self._controller = SimpleEventDispatcherConfigController(config)

    @property
    def interface(self) -> SimpleEventDispatcherConfigInterface:
        """Impide el control, pero permite mostrar los atributos a alguien no autorizado a modificarlos."""
        return self._interface

    @property
    def controller(self) -> SimpleEventDispatcherConfigController:
        """Otorga control permitiendo modificar la configuración"""
        return self._controller
