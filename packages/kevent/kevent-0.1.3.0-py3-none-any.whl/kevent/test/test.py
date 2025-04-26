from kevent.dispatcher.simple import SimpleEventDispatcher
from kevent.dispatcher.simple.dispatcher.config import SimpleEventDispatcherConfig
from kevent.event import Event


def test():
    from kevent.dispatcher.simple.callback import SimpleEventCallback

    class SampleEvent(Event):
        ...

    class ConcreteEventA(SampleEvent):
        integer: int

    class ConcreteEventB(SampleEvent):
        string: str

    class UnknownConcreteEvent(SampleEvent):
        ...

    def sample_callback(event: SampleEvent):
        print(f'Event: {event}')

    event_types = [ConcreteEventA, ConcreteEventB]
    config = SimpleEventDispatcherConfig(allow_multiple=False)
    dispatcher: SimpleEventDispatcher[SampleEvent] = SimpleEventDispatcher(event_types, config=config)

    lmda = lambda e: sample_callback(e)
    dispatcher.subscribe(ConcreteEventA, SimpleEventCallback(sample_callback))
    dispatcher.subscribe(ConcreteEventB, lmda)

    sample_events = (ConcreteEventA(integer=1), ConcreteEventB(string='test'), ConcreteEventB(string='nandemo'))
    dispatcher.enable(False)
    dispatcher.dispatch(sample_events)
    dispatcher.enable()
    dispatcher.dispatch()


if __name__ == '__main__':
    test()