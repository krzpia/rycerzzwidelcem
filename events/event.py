class Event:

    def __init__(self, id: str) -> None:
        self.id = id

    def __eq__(self, other: 'Event') -> bool:
        return self.id == other.id
