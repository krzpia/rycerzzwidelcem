import unittest

from dialogs import Dialog


class TestDialog(unittest.TestCase):

    def test_dialog_can_have_npc_lines(self) -> None:
        Dialog()
