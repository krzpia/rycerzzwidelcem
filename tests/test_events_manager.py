import unittest


class EventManager:
    
    def emit(self):
        pass


class TestEventManager(unittest.TestCase):

    def test_manager_can_emit_event(self) -> None:
        EventManager().emit()