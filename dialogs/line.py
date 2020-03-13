import abc


class Line(abc.ABC):

    def __init__(self, text: str) -> None:
        self.text = text

    @abc.abstractmethod
    def belongs_to_npc(self) -> bool:
        pass

    def __eq__(self, other: 'Line') -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.text == other.text


class NpcLine(Line):

    def belongs_to_npc(self) -> bool:
        return True


class PlayerLine(Line):

    def belongs_to_npc(self) -> bool:
        return False
