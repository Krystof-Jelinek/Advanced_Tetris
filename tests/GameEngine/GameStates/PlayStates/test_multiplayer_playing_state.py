"""
Tests for the MultiplayerPlayingState.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from src.GameEngine.GameStates.PlayStates.multiplayer_playing_state import MultiplayerPlayingState


@pytest.fixture
def mock_messaging():
    """Fixture providing a mocked messaging system."""
    return MagicMock()


@pytest.fixture
def mock_event_bus():
    """Fixture providing a mocked event bus."""
    return MagicMock()


@pytest.fixture
def multiplayer_state(mock_messaging, mock_event_bus):
    """Fixture providing a MultiplayerPlayingState with mocked audio."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_music'):
        return MultiplayerPlayingState(mock_messaging, mock_event_bus)


def test_multiplayer_playing_state_initialization(multiplayer_state):
    """Test initial configuration of multiplayer-specific components."""
    assert multiplayer_state.enemy_board is not None
    assert multiplayer_state.enemy_score_board is not None
    assert multiplayer_state.enemy_still_playing


def test_multiplayer_playing_state_update(multiplayer_state, mock_messaging):
    """Test that updating sends the current game state to the opponent."""
    with patch('src.GameEngine.GameStates.PlayStates.playing_state.PlayingState.update') as mock_super_update:
        mock_super_update.return_value = multiplayer_state
        multiplayer_state.update(0.1, MagicMock())

        mock_messaging.send_message.assert_called_once()
        sent_msg = mock_messaging.send_message.call_args[0][0]
        # pylint: disable=import-outside-toplevel
        from src.MessagingSystem.GameMessages.game_state_message import GameStateMessage
        assert isinstance(sent_msg, GameStateMessage)


def test_multiplayer_playing_state_game_over(multiplayer_state, mock_messaging):
    """Test game over transition and notification in multiplayer."""
    with patch('src.GameEngine.GameStates.PlayStates.multiplayer_waiting_for_enemy_end_state.MultiplayerWaitingForEnemyEndState') as mock_wait_state:
        multiplayer_state.game_over()
        mock_messaging.send_message.assert_called_once()
        assert multiplayer_state.next_state == mock_wait_state.return_value


def test_multiplayer_playing_state_enemy_updates(multiplayer_state):
    """Test updating the local representation of the opponent's state."""
    multiplayer_state.update_enemy_score(1000)
    assert multiplayer_state.enemy_score_board.get_score() == 1000

    multiplayer_state.on_enemy_ended()
    assert not multiplayer_state.enemy_still_playing
