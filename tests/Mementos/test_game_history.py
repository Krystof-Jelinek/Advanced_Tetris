"""
Tests for the GameHistory caretaker.
"""
# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from src.Mementos.Caretakers.game_history import GameHistory


@pytest.fixture
def originator():
    """Fixture providing a mocked originator whose mementos are numbered 1, 2, 3, ..."""
    mock = MagicMock()
    mock.create_memento.side_effect = range(1, 10_000)
    return mock


def test_records_once_per_interval(originator):
    """With 60 frames per second and a 0.05 s interval, every third frame is saved."""
    history = GameHistory(seconds=30.0, interval=0.05)
    for _ in range(60):
        history.record(1 / 60, originator)
    assert len(history) == 20
    assert originator.create_memento.call_count == 20


def test_keeps_only_the_last_seconds(originator):
    """The oldest mementos are dropped, so the history covers at most `seconds` of play."""
    history = GameHistory(seconds=1.0, interval=0.1)
    for _ in range(50):
        history.record(0.1, originator)
    assert len(history) == 10
    assert [history.pop_latest() for _ in range(10)] == list(range(50, 40, -1))


def test_pop_latest_newest_first_then_none(originator):
    """Mementos come back newest first; an empty history returns None."""
    history = GameHistory(seconds=1.0, interval=0.1)
    for _ in range(3):
        history.record(0.1, originator)
    assert [history.pop_latest() for _ in range(4)] == [3, 2, 1, None]


def test_nothing_recorded_before_the_interval(originator):
    """A frame shorter than the interval does not save anything yet."""
    history = GameHistory(seconds=1.0, interval=0.1)
    history.record(0.05, originator)
    assert len(history) == 0
    originator.create_memento.assert_not_called()
