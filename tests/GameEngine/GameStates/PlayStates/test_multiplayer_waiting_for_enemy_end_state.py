"""
Tests for the MultiplayerWaitingForEnemyEndState.
"""
from unittest.mock import MagicMock, patch
from src.GameEngine.GameStates.PlayStates.multiplayer_waiting_for_enemy_end_state import MultiplayerWaitingForEnemyEndState


def test_multiplayer_waiting_for_enemy_end_state_update_still_playing():
    """Test that the state continues waiting while the opponent is still playing."""
    mock_wrapped = MagicMock()
    mock_wrapped.is_enemy_playing.return_value = True

    state = MultiplayerWaitingForEnemyEndState(mock_wrapped)

    with patch('src.MessagingSystem.GameMessages.game_state_message.GameStateMessage.create_message') as _mock_create_msg:
        res = state.update(0.1, MagicMock())
        assert res == state
        mock_wrapped.update.assert_called_once()
        mock_wrapped.messaging_system.send_message.assert_called_once()


def test_multiplayer_waiting_for_enemy_end_state_transition_to_game_over():
    """Test transitioning to the results screen once the opponent finishes."""
    mock_wrapped = MagicMock()
    mock_wrapped.is_enemy_playing.return_value = True
    state = MultiplayerWaitingForEnemyEndState(mock_wrapped)

    # Enemy ends
    state.on_enemy_ended()

    with patch('src.GameEngine.GameStates.PlayStates.multiplayer_waiting_for_enemy_end_state.MultiplayerGameOverState') as mock_game_over:
        res = state.update(0.1, MagicMock())
        assert res == mock_game_over.return_value
