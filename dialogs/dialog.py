import typing

from dialogs.line import Line
from dialogs.line import NpcLine
from dialogs.line import PlayerLine


class Dialog:

    def __init__(self) -> None:
        self.setup_stage = 0
        self.lines: typing.List[Line] = []
        self.lines_by_stage: typing.Dict[int, typing.List[Line]] = {
            self.setup_stage: []
        }

    def add_npc_line(self, text: str) -> None:
        self.lines.append(NpcLine(text))
        self.lines_by_stage[self.setup_stage].append(NpcLine(text))

    def add_player_line(self, text: str) -> None:
        self.lines.append(PlayerLine(text))
        self.lines_by_stage[self.setup_stage].append(PlayerLine(text))

    def lines_for_stage(self, stage: int) -> typing.List[Line]:
        return self.lines_by_stage[stage]
