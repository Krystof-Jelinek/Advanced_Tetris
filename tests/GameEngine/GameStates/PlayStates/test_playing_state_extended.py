"""
Extended tests for the PlayingState, including abilities and explosions.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


@pytest.fixture
def mock_event_bus():
    """Fixture providing a mocked event bus."""
    return MagicMock()


@pytest.fixture
def playing_state(mock_event_bus):
    """Fixture providing a PlayingState with mocked audio."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_music'):
        return PlayingState(mock_event_bus)


def test_playing_state_add_garbage_lines(playing_state):
    """Test that garbage lines are correctly added to the board."""
    playing_state.add_garbage_lines(num_lines=2, duration=10.0)
    # Check if first 2 rows are TimeLockedSquares
    # pylint: disable=import-outside-toplevel
    from src.GameComponents.TetrisSquares.time_locked_square import TimeLockedSquare
    assert isinstance(playing_state.board.grid[0][0], TimeLockedSquare)
    assert isinstance(playing_state.board.grid[1][0], TimeLockedSquare)


def test_playing_state_on_piece_explosion(playing_state):
    """Test that a piece explosion triggers a transition to SquareClearingState."""
    # Place something clearable at 5,5
    # pylint: disable=import-outside-toplevel
    from src.GameComponents.TetrisSquares.piece_square import PieceSquare
    playing_state.board.grid[5][5] = PieceSquare(5, 5, 0, 0, (255, 255, 255))

    playing_state.current_piece.center_square.grid_row = 5
    playing_state.current_piece.center_square.grid_col = 5

    with patch('src.GameEngine.GameStates.PlayStates.square_clearing_state.SquareClearingState') as mock_clear_state:
        playing_state.on_piece_explosion({})
        # Should transition to SquareClearingState
        assert playing_state.next_state == mock_clear_state.return_value
