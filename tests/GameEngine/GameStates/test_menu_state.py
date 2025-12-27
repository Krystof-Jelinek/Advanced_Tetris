"""
Tests for the MenuState.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
import pytest
from src.GameEngine.GameStates.Menus.menu_state import MenuState


@pytest.fixture
def menu_state():
    """Fixture providing a MenuState with a mocked game manager."""
    mock_manager = MagicMock()
    return MenuState(mock_manager), mock_manager


def test_menu_state_initialization(menu_state):
    """Test initial configuration of the menu state."""
    state, _manager = menu_state
    assert len(state.options) == 2
    assert state.selected_index == 0
    assert state.next_state == state


def test_menu_state_move_down(menu_state):
    """Test navigating down through menu options."""
    state, _ = menu_state
    state.on_move_down()
    assert state.selected_index == 1
    state.on_move_down()
    assert state.selected_index == 0  # Loop back


def test_menu_state_move_up(menu_state):
    """Test navigating up through menu options."""
    state, _ = menu_state
    state.on_move_up()
    assert state.selected_index == 1  # Loop back to last
    state.on_move_up()
    assert state.selected_index == 0


def test_menu_state_update(menu_state):
    """Test that update correctly sets the selected attribute on options."""
    state, _ = menu_state
    state.selected_index = 1
    state.update(0.1, MagicMock())
    assert not state.options[0].selected
    assert state.options[1].selected


def test_menu_state_on_select_option(menu_state):
    """Test executing the selected menu option."""
    state, manager = menu_state
    mock_new_state = MagicMock()
    state.options[0].create_state = MagicMock(return_value=mock_new_state)

    state.on_select_option()
    assert state.next_state == mock_new_state
    state.options[0].create_state.assert_called_once_with(manager)
