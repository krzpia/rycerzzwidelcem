import unittest

from events.event import Event


class TestEvent(unittest.TestCase):

    def test_event_string_representation(self) -> None:
        self.assertEqual(
            repr(Event('Rat has been killed')),
            "Event(id='Rat has been killed')",
        )