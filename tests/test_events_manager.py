import unittest

import typing

Subscriber = typing.Callable[['Event'], None]

class EventManager:

    def __init__(self) -> None:
        self.subscribers: typing.List[Subscriber] = []
        self.events = []

    def emit(self, event: 'Event') -> None:
        self.events.append(event)
        for subscriber in self.subscribers:
            subscriber(event)

    def subscribe(self, callback: Subscriber) -> None:
        self.subscribers.append(callback)


class Event:

    def __eq__(self, other: 'Event') -> bool:
        return True


class TestEventManager(unittest.TestCase):

    def test_manager_can_emit_event(self) -> None:
        manager = EventManager()
        manager.emit(Event())
        assert manager.events == [Event()]

    def test_manager_publishes_events_to_subscribers(self) -> None:
        subscriber = SpySubscriber()
        manager = EventManager()
        manager.subscribe(subscriber.receive)
        manager.emit(Event())
        assert subscriber.events == [Event()]


class SpySubscriber:

    def __init__(self) -> None:
        self.events = []

    def receive(self, event: 'Event') -> None:
        self.events.append(event)
