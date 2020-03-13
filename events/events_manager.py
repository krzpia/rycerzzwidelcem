import typing

from .event import Event

Subscriber = typing.Callable[['Event'], None]


class EventManager:

    def __init__(self) -> None:
        self.subscribers: typing.List[Subscriber] = []
        self.events: typing.List[Event] = []

    def emit(self, event: 'Event') -> None:
        self.events.append(event)
        for subscriber in self.subscribers:
            subscriber(event)

    def subscribe(self, callback: Subscriber) -> None:
        self.subscribers.append(callback)

    def history(self) -> typing.List['Event']:
        return self.events[::-1]
