import typing

from dialogs.line import Line
from dialogs.line import NpcLine
from dialogs.line import PlayerLine


class Dialog:

    def __init__(self) -> None:
        self.lines: typing.List[Line] = []

    def add_npc_line(self, text: str) -> None:
        self.lines.append(NpcLine(text))

    def add_player_line(self, text: str) -> None:
        self.lines.append(PlayerLine(text))
