class Event:

    def __init__(self, id: str) -> None:
        self.id = id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id!r})'
