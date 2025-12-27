"""
Tests for the EventBus class.
"""
from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameEvents.events import GameEvent


def test_event_bus_subscribe_and_push():
    """Test subscribing a callback and pushing an event with data."""
    bus = EventBus()
    called_with = None

    def callback(data):
        nonlocal called_with
        called_with = data

    bus.subscribe(GameEvent.LINES_CLEARED, callback)
    bus.push_event(GameEvent.LINES_CLEARED, {"rows": 4})

    assert called_with == {"rows": 4}


def test_event_bus_unsubscribe():
    """Test unsubscribing a callback so it no longer receives events."""
    bus = EventBus()
    call_count = 0

    def callback(_data):
        nonlocal call_count
        call_count += 1

    bus.subscribe(GameEvent.LINES_CLEARED, callback)
    bus.push_event(GameEvent.LINES_CLEARED)
    assert call_count == 1

    bus.unsubscribe(GameEvent.LINES_CLEARED, callback)
    bus.push_event(GameEvent.LINES_CLEARED)
    assert call_count == 1


def test_event_bus_multiple_listeners():
    """Test that multiple listeners can subscribe to the same event."""
    bus = EventBus()
    calls = []

    bus.subscribe(GameEvent.LINES_CLEARED, lambda d: calls.append(1))
    bus.subscribe(GameEvent.LINES_CLEARED, lambda d: calls.append(2))

    bus.push_event(GameEvent.LINES_CLEARED)
    assert 1 in calls
    assert 2 in calls
    assert len(calls) == 2
