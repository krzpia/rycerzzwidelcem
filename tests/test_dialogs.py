import unittest

from dialogs import Dialog


class TestDialog(unittest.TestCase):

    def test_dialog_can_have_npc_lines(self) -> None:
        dialog = Dialog()
        dialog.add_npc_line("I'm Npc. What's your name?")
        assert dialog.lines == ["I'm Npc. What's your name?"]

    def test_dialog_can_have_player_lines(self) -> None:
        dialog = Dialog()
        dialog.add_player_line("I'm the player.")
        assert dialog.lines == ["I'm the player."]
