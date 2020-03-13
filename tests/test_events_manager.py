import unittest


class EventManager:
    pass


class TestEventManager(unittest.TestCase):

    def test_manager_can_emit_event(self) -> None:
        EventManager