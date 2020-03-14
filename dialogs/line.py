import abc


class Line(abc.ABC):

    def __init__(self, text: str) -> None:
        self.text = text

    @abc.abstractmethod
    def belongs_to_npc(self) -> bool:
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.text == other.text

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text={self.text!r})'


class NpcLine(Line):

    def belongs_to_npc(self) -> bool:
        return True


class PlayerLine(Line):

    def belongs_to_npc(self) -> bool:
        return False
