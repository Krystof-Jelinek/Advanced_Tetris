"""
Tests for the core PlayingState.
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


def test_playing_state_initialization(playing_state):
    """Test initial state of gameplay components."""
    assert playing_state.board is not None
    assert playing_state.current_piece is not None
    assert playing_state.score_board is not None
    assert playing_state.difficulty.drop_interval == 1.0


def test_playing_state_get_drop_interval(playing_state):
    """Test that drop interval decreases over time and respects modifiers."""
    # Initial interval
    assert playing_state.get_drop_interval() == 1.0
    # After some time
    playing_state.difficulty.time_elapsed = 300  # 5 minutes
    interval = playing_state.get_drop_interval()
    assert 0.1 < interval < 1.0

    # With time modifier
    playing_state.update_time_modifier(0.5)
    assert playing_state.get_drop_interval() == interval * 0.5


def test_playing_state_update(playing_state):
    """Test that update triggers piece movement when the drop timer expires."""
    playing_state.difficulty.drop_timer = 0.99
    playing_state.difficulty.drop_interval = 1.0

    with patch.object(playing_state, 'move_current_piece_down') as mock_move:
        playing_state.update(0.02, MagicMock())
        assert playing_state.difficulty.drop_timer == 0.0  # Reset
        mock_move.assert_called_once()


def test_playing_state_on_move_right(playing_state):
    """Test that input methods trigger the corresponding game actions."""
    with patch('src.GameEngine.GameStates.PlayStates.playing_state.MovePieceRight') as mock_action:
        playing_state.on_move_right()
        mock_action.return_value.execute.assert_called_once()
