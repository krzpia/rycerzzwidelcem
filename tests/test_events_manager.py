import unittest

import typing
from events.event import Event

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

    def history(self) -> typing.List['Event']:
        return self.events[::-1]


class TestEventManager(unittest.TestCase):

    def test_manager_can_emit_event(self) -> None:
        manager = EventManager()
        manager.emit(Event('Rat killed'))
        assert manager.events == [Event('Rat killed')]

    def test_manager_publishes_events_to_subscribers(self) -> None:
        subscriber = SpySubscriber()
        manager = EventManager()
        manager.subscribe(subscriber.receive)
        manager.emit(Event('Rat killed'))
        assert subscriber.events == [Event('Rat killed')]

    def test_returns_story_of_events_from_a_newest_to_the_last(self) -> None:
        manager = EventManager()
        manager.emit(Event('Rat killed'))
        manager.emit(Event('Quest completed'))
        assert (
            manager.history() == [Event('Quest completed'), Event('Rat killed')]
        )


class SpySubscriber:

    def __init__(self) -> None:
        self.events = []

    def receive(self, event: 'Event') -> None:
        self.events.append(event)
