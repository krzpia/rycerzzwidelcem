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

    def search_event(self, search_event) -> bool:
        for game_event in self.events:
            if game_event.id == search_event:
                return True

    def return_killed_mobs_names(self) -> list:
        mobs_killed = []
        for game_event in self.events:
            if game_event.id[-15:] == "has been killed":
                print(f'"Appending {game_event.id[:-16]} to mobs_killed list')
                mobs_killed.append(game_event.id[:-16])
        return mobs_killed

    def find_npc_encounter_event(self, npc_name) -> bool:
        for game_event in self.events:
            if game_event.id == f'{npc_name} has been encountered':
                return True

    def find_got_quest_event(self, quest_name) -> bool:
        for game_event in self.events:
            if game_event.id == f'got quest {quest_name}':
                return True

    def find_quest_compl_event(self, quest_name) -> bool:
        #print ("SEARCHING IN EVENTS TO FIND quest xxxx has been completed")
        for game_event in self.events:
            if game_event.id == f'quest {quest_name} has been completed':
                #print ("SEARCHING IN EVENTS TO FIND quest xxxxx has been completed = True.")
                return True

    def find_quest_rewarded_event(self, quest_name) -> bool:
        for game_event in self.events:
            if game_event.id == f'quest {quest_name} has been rewarded':
                return True

    def find_thread_read_event(self, thread_name) -> bool:
        for game_event in self.events:
            if game_event.id == f'thread {thread_name} has been read':
                return True




