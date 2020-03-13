import unittest

from dialogs.line import NpcLine
from dialogs.line import PlayerLine


class TestLine(unittest.TestCase):

    def test_npc_line_knows_its_owner(self) -> None:
        assert NpcLine("I'm Npc!").belongs_to_npc()

    def test_player_line_knows_its_owner(self) -> None:
        self.assertFalse(PlayerLine("I'm Player!").belongs_to_npc())

    def test_line_equal_if_text_and_type_equal(self) -> None:
        self.assertEqual(NpcLine('text'), NpcLine('text'))

    def test_line_different_if_text_equal_but_types_differ(self) -> None:
        self.assertNotEqual(NpcLine('text'), PlayerLine('text'))
