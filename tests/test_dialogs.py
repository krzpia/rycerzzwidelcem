import unittest

from dialogs.dialog import Dialog
from dialogs.line import NpcLine
from dialogs.line import PlayerLine
from events.event import Event


class TestDialog(unittest.TestCase):

    def test_dialog_can_have_npc_lines(self) -> None:
        dialog = Dialog()
        dialog.add_npc_line("I'm Npc. What's your name?")
        assert next(dialog.lines()) == NpcLine("I'm Npc. What's your name?")

    def test_dialog_can_have_player_lines(self) -> None:
        dialog = Dialog()
        dialog.add_player_line("I'm the player.")
        assert next(dialog.lines()) == PlayerLine("I'm the player.")

    def test_dialog_are_added_to_initial_stage(self) -> None:
        dialog = Dialog()
        dialog.add_player_line("I'm the player.")
        self.assertEqual(
            dialog.lines_for_stage(0), [PlayerLine("I'm the player.")]
        )

    def test_dialogs_are_added_to_previously_defined_stage(self) -> None:
        dialog = Dialog()
        dialog.add_player_line("I'm the player.")
        dialog.set_next_stage(fired_by=Event('Rat killed'))
        dialog.add_npc_line("I'm Npc. You have killed a rat")
        dialog.add_player_line("Yes I did!")
        dialog.set_next_stage(fired_by=Event('Huge Rat killed'))
        dialog.add_npc_line("Wow you have killed a Huuuge rat")
        self.assertEqual(
            dialog.lines_for_stage(0), [PlayerLine("I'm the player.")]
        )
        self.assertEqual(
            dialog.lines_for_stage(1),
            [
                NpcLine("I'm Npc. You have killed a rat"),
                PlayerLine("Yes I did!"),
            ]
        )
        self.assertEqual(
            dialog.lines_for_stage(2),
            [NpcLine("Wow you have killed a Huuuge rat")]
        )

    def test_presents_lines_for_initial_stage(self) -> None:
        dialog = Dialog()
        dialog.add_player_line("I'm the player.")
        dialog.set_next_stage(fired_by=Event('Rat killed'))
        dialog.add_npc_line("I'm Npc. You have killed a rat")
        dialog.add_player_line("Yes I did!")
        lines = dialog.lines()
        self.assertEqual(next(lines), PlayerLine("I'm the player."))
        with self.assertRaises(StopIteration):
            next(lines)

    def test_presents_line_for_next_stage_if_specific_event_happened(
            self) -> None:
        dialog = Dialog()
        dialog.add_player_line("I'm the player.")
        dialog.set_next_stage(fired_by=Event('Rat killed'))
        dialog.add_npc_line("I'm Npc. You have killed a rat")
        dialog.add_player_line("Yes I did!")
        dialog.handle(event=Event('Rat killed'))
        lines = dialog.lines()
        self.assertEqual(next(lines), NpcLine("I'm Npc. You have killed a rat"))
        self.assertEqual(next(lines), PlayerLine("Yes I did!"))
        with self.assertRaises(StopIteration):
            next(lines)

    def test_only_specified_events_trigger_stage_change(self) -> None:
        dialog = Dialog()
        dialog.add_player_line("I'm the player.")
        dialog.set_next_stage(fired_by=Event('Rat killed'))
        dialog.add_npc_line("I'm Npc. You have killed a rat")
        dialog.handle(event=Event('Item found'))
        lines = dialog.lines()
        self.assertEqual(next(lines), PlayerLine("I'm the player."))

    def test_triggering_events_has_to_happen_in_order(self) -> None:
        dialog = Dialog()
        dialog.add_player_line("I'm the player.")
        dialog.set_next_stage(fired_by=Event('Rat killed'))
        dialog.add_npc_line("I'm Npc. You have killed a rat")
        dialog.set_next_stage(fired_by=Event('Item found'))
        dialog.handle(event=Event('Item found'))
        lines = dialog.lines()
        self.assertEqual(next(lines), PlayerLine("I'm the player."))
