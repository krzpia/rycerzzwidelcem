class Dialog:

    def __init__(self) -> None:
        self.lines = []

    def add_npc_line(self, text: str) -> None:
        self.lines.append(text)

    def add_player_line(self, text: str) -> None:
        self.lines.append(text)
