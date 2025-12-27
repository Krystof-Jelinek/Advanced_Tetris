"""
Tests for the TimeLockedSquare class.
"""
from src.GameComponents.TetrisSquares.time_locked_square import TimeLockedSquare


def test_time_locked_square_initialization():
    """Test initial state of a time-locked square."""
    square = TimeLockedSquare(0, 0, duration=10.0)
    assert square.is_locked
    assert square.timer == 10.0
    assert not square.is_clearable()
    assert not square.is_scorable()


def test_time_locked_square_update():
    """Test updating the timer and unlocking the square."""
    square = TimeLockedSquare(0, 0, duration=10.0)

    # Update with 5 seconds
    square.update(5.0)
    assert square.timer == 5.0
    assert square.is_locked
    assert not square.is_clearable()

    # Update with another 6 seconds (total 11)
    square.update(6.0)
    assert square.timer == 0
    assert not square.is_locked
    assert square.is_clearable()


def test_time_locked_square_near_zero_duration():
    """Test unlocking when update duration exceeds remaining time."""
    # Testing that it unlocks when timer reaches zero from a positive value
    square = TimeLockedSquare(0, 0, duration=0.01)
    assert square.is_locked

    square.update(0.02)
    assert not square.is_locked
    assert square.is_clearable()
