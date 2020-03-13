import abc


class Line(abc.ABC):

    def __init__(self, text: str) -> None:
        self.text = text

    @abc.abstractmethod
    def belongs_to_npc(self) -> bool:
        pass


class NpcLine(Line):

    def belongs_to_npc(self) -> bool:
        return True
