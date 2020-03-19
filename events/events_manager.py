import typing

from .event import Event

Subscriber = typing.Callable[['Event'], None]


class EventManager:

    def __init__(self) -> None:
        self.subscribers: typing.List[Subscriber] = []
        self.subscribers_by_id: typing.Dict[str, Subscriber] = {}
        self.events: typing.List[Event] = []

    def emit(self, event: 'Event') -> None:
        self.events.append(event)
        for subscriber in self.subscribers:
            subscriber(event)
        try:
            self.subscribers_by_id[event.id](event)
        except KeyError:
            pass

    def subscribe(self, callback: Subscriber) -> None:
        self.subscribers.append(callback)

    def subsribe_for_event(self, id: str, callback: Subscriber) -> None:
        self.subscribers_by_id[id] = callback

    def history(self) -> typing.List['Event']:
        return self.events[::-1]

    def find_npc_encounter_event(self, npc_name) -> bool:
        for game_event in self.events:
            if game_event.id == f'{npc_name} has been encountered.':
                return True
