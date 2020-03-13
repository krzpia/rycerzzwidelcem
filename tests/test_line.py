import unittest

from dialogs.line import NpcLine


class TestLine(unittest.TestCase):

    def test_npc_line_knows_its_owner(self) -> None:
        assert NpcLine("I'm Npc!").belongs_to_npc()