import unittest


class EventManager:

    def __init__(self) -> None:
        self.events = []

    def emit(self, event: 'Event') -> None:
        self.events.append(event)


class Event:

    def __eq__(self, other: 'Event') -> bool:
        return True


class TestEventManager(unittest.TestCase):

    def test_manager_can_emit_event(self) -> None:
        manager = EventManager()
        manager.emit(Event())
        assert manager.events == [Event()]
