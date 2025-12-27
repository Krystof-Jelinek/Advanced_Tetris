"""
Tests for the GameOverState.
"""
from unittest.mock import MagicMock, patch
from src.GameEngine.GameStates.PlayStates.game_over_state import GameOverState


def test_game_over_state_initialization():
    """Test initial configuration and audio triggers of the game over state."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.stop_music'), \
         patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_sound'):
        state = GameOverState(score=500)
        assert state.scoreboard.get_score() == 500


def test_game_over_state_on_reset():
    """Test resetting the game from the game over screen."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.stop_music'), \
         patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_sound'):
        state = GameOverState(score=500)
        mock_manager = MagicMock()
        state.on_reset(mock_manager)
        mock_manager.reset_self.assert_called_once()
