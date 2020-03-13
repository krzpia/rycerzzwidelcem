import typing

from dialogs.line import Line
from dialogs.line import NpcLine
from dialogs.line import PlayerLine
from events.event import Event


class Dialog:

    def __init__(self) -> None:
        self.triggers: typing.List[Event] = []
        self.stage = 0
        self.setup_stage = 0
        self.lines_by_stage: typing.Dict[int, typing.List[Line]] = {
            self.setup_stage: []
        }

    def add_npc_line(self, text: str) -> None:
        self.lines_by_stage[self.setup_stage].append(NpcLine(text))

    def add_player_line(self, text: str) -> None:
        self.lines_by_stage[self.setup_stage].append(PlayerLine(text))

    def lines_for_stage(self, stage: int) -> typing.List[Line]:
        return self.lines_by_stage[stage]

    def set_next_stage(self, fired_by: Event) -> None:
        self.setup_stage += 1
        self.lines_by_stage[self.setup_stage] = []
        self.triggers.append(fired_by)

    def lines(self) -> typing.Generator[Line, None, None]:
        for line in self.lines_by_stage[self.stage]:
            yield line

    def handle(self, event: Event) -> None:
        if self.triggers and event == self.triggers[-1]:
            self.triggers.pop()
            self.stage += 1
