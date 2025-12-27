"""
Tests for the SquareClearingState.
"""
from unittest.mock import MagicMock
from src.GameEngine.GameStates.PlayStates.square_clearing_state import SquareClearingState


def test_square_clearing_state_initialization():
    """Test sorting and storage of squares to be cleared."""
    mock_wrapped = MagicMock()
    mock_wrapped.board = MagicMock()
    squares = [(5, 5), (6, 5)]
    state = SquareClearingState(mock_wrapped, squares)

    # Should be sorted by row descending
    assert state.squares_to_clear == [(6, 5), (5, 5)]
    assert len(state.squares_to_clear) == 2


def test_square_clearing_state_update_blinking():
    """Test that update triggers blinking animation on the board squares."""
    mock_wrapped = MagicMock()
    mock_board = MagicMock()
    mock_square = MagicMock()
    mock_board.__getitem__.return_value.__getitem__.return_value = mock_square
    mock_wrapped.board = mock_board

    state = SquareClearingState(mock_wrapped, [(5, 5)])
    state.blink_interval = 0.1

    # Update triggered blink
    state.update(0.11, MagicMock())
    assert state.blink_count == 1
    mock_square.toggle_blink.assert_called_once()


def test_square_clearing_state_finish():
    """Test that the state finishes after the maximum number of blinks and clears squares."""
    mock_wrapped = MagicMock()
    mock_board = MagicMock()
    mock_wrapped.board = mock_board

    state = SquareClearingState(mock_wrapped, [(5, 5)])
    state.blink_count = 5
    state.max_blinks = 6
    state.blink_interval = 0.1

    result = state.update(0.11, MagicMock())

    assert state.blink_count == 6
    mock_board.clear_square.assert_called_with(5, 5)
    assert result == mock_wrapped
