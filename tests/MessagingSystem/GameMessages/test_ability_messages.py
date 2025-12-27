"""
Tests for ability-related game messages.
"""
from unittest.mock import MagicMock, patch
from src.MessagingSystem.GameMessages.AbilityMessages.garbage_ability_message import GarbageLinesMessage
from src.MessagingSystem.GameMessages.AbilityMessages.speed_up_time_message import SpeedUpTimeMessage


def test_garbage_lines_message_execute():
    """Test executing a garbage lines message on the game state."""
    msg = GarbageLinesMessage()
    mock_manager = MagicMock()
    mock_state = MagicMock()
    mock_state.is_ability_wrappable.return_value = True
    mock_manager.get_game_state.return_value = mock_state

    msg.execute(mock_manager)
    mock_state.add_garbage_lines.assert_called_once_with(3, 20.0)


def test_speed_up_time_message_execute():
    """Test executing a speed up time message by wrapping the game state."""
    msg = SpeedUpTimeMessage()
    mock_manager = MagicMock()
    mock_state = MagicMock()
    mock_state.is_ability_wrappable.return_value = True
    mock_manager.get_game_state.return_value = mock_state

    with patch('src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.time_speed_modification_state.TimeSpeedModificationState') as mock_wrap_state:
        msg.execute(mock_manager)
        mock_manager.set_game_state.assert_called_once_with(mock_wrap_state.return_value)
