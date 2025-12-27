"""
Tests for the MultiplayerMenuState.
"""
from unittest.mock import MagicMock
from src.GameEngine.GameStates.Menus.multiplayer_menu_state import MultiplayerMenuState


def test_multiplayer_menu_state_initialization():
    """Test initial configuration of the multiplayer menu."""
    mock_manager = MagicMock()
    state = MultiplayerMenuState(mock_manager)
    assert len(state.options) == 2
    assert state.selected_index == 0


def test_multiplayer_menu_state_navigation():
    """Test navigating through multiplayer menu options."""
    mock_manager = MagicMock()
    state = MultiplayerMenuState(mock_manager)

    state.on_move_down()
    assert state.selected_index == 1

    state.on_move_up()
    assert state.selected_index == 0


def test_multiplayer_menu_state_on_select_option():
    """Test executing the selected multiplayer menu option."""
    mock_manager = MagicMock()
    state = MultiplayerMenuState(mock_manager)

    mock_new_state = MagicMock()
    state.options[0].create_state = MagicMock(return_value=mock_new_state)

    state.on_select_option()
    assert state.next_state == mock_new_state
