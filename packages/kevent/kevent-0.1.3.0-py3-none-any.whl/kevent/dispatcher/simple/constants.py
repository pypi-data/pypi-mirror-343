from typing import Callable, ParamSpec, TypeVar

from kevent.event import EVENT_T

P = ParamSpec("P")
R = TypeVar("R")
CALLABLE_T = Callable[[EVENT_T], None]
