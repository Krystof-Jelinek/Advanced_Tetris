"""
Tests for various MenuOption subclasses (SinglePlayer, Multiplayer, Host, Join).
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from src.GameEngine.GameStates.Menus.MenuOptions.single_player_option import SinglePlayerOption
from src.GameEngine.GameStates.Menus.MenuOptions.multi_player_option import MultiPlayerOption
from src.GameEngine.GameStates.Menus.MenuOptions.host_option import HostOption
from src.GameEngine.GameStates.Menus.MenuOptions.join_option import JoinOption


@pytest.fixture
def mock_manager():
    """Fixture providing a mocked game manager."""
    return MagicMock()


def test_single_player_option(mock_manager):
    """Test that SinglePlayerOption creates an AbilitySelectState with 'SINGLE' mode."""
    option = SinglePlayerOption()
    assert option.text == "Single Player"
    with patch('src.GameEngine.GameStates.Menus.MenuOptions.single_player_option.AbilitySelectState') as mock_state:
        state = option.create_state(mock_manager)
        assert state == mock_state.return_value
        mock_state.assert_called_once_with(mock_manager, "SINGLE")


def test_multi_player_option(mock_manager):
    """Test that MultiPlayerOption creates an AbilitySelectState with 'MULTI' mode."""
    option = MultiPlayerOption()
    assert option.text == "Multiplayer"
    with patch('src.GameEngine.GameStates.Menus.MenuOptions.multi_player_option.AbilitySelectState') as mock_state:
        state = option.create_state(mock_manager)
        assert state == mock_state.return_value
        mock_state.assert_called_once_with(mock_manager, "MULTI")


def test_host_option(mock_manager):
    """Test that HostOption triggers multiplayer hosting and returns the correct state."""
    option = HostOption()
    with patch('src.GameEngine.GameStates.Menus.MenuOptions.host_option.WaitingForConnectionState') as mock_state:
        state = option.create_state(mock_manager)
        mock_manager.start_multiplayer.assert_called_once()
        assert state == mock_state.return_value


def test_join_option(mock_manager):
    """Test that JoinOption triggers multiplayer joining and returns the correct state."""
    option = JoinOption()
    with patch('src.GameEngine.GameStates.Menus.MenuOptions.join_option.IPInputState') as mock_state:
        state = option.create_state(mock_manager)
        mock_manager.start_multiplayer.assert_called_once()
        assert state == mock_state.return_value
