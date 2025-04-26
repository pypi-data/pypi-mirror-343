from abc import ABC
from typing import TypeVar

from kmodels.models import CoreModel
from pydantic import ConfigDict


class Event(CoreModel, ABC):
    model_config = ConfigDict(frozen=True, extra='forbid')


# Tipo genérico para eventos
EVENT_T = TypeVar('EVENT_T', bound=Event)
