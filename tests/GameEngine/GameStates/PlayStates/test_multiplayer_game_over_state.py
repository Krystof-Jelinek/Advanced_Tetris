"""
Tests for the MultiplayerGameOverState.
"""
from unittest.mock import MagicMock, patch
from src.GameEngine.GameStates.PlayStates.multiplayer_game_over_state import MultiplayerGameOverState


def test_multiplayer_game_over_state_initialization():
    """Test initial configuration and score storage in multiplayer game over."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.stop_music'), \
         patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_sound'):
        state = MultiplayerGameOverState(my_score=1000, enemy_score=800)
        assert state.my_score == 1000
        assert state.enemy_score == 800


def test_multiplayer_game_over_state_on_reset():
    """Test resetting the game from the multiplayer results screen."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.stop_music'), \
         patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_sound'):
        state = MultiplayerGameOverState(100, 200)
        mock_manager = MagicMock()
        state.on_reset(mock_manager)
        mock_manager.reset_self.assert_called_once()
