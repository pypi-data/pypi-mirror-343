from kevent.dispatcher.simple.callback import SimpleEventCallback
from kevent.dispatcher.simple.constants import CALLABLE_T
from kevent.event import EVENT_T

CALLBACK_T = SimpleEventCallback[EVENT_T] | CALLABLE_T
