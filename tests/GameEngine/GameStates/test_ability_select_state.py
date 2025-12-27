"""
Tests for the AbilitySelectState.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from src.GameEngine.GameStates.Menus.ability_select_state import AbilitySelectState


@pytest.fixture
def ability_state():
    """Fixture providing an AbilitySelectState with mocked dependencies."""
    mock_manager = MagicMock()
    # Mocking PlayingState and MultiplayerMenuState to avoid massive imports/logic
    with patch('src.GameEngine.GameStates.Menus.ability_select_state.PlayingState'), \
         patch('src.GameEngine.GameStates.Menus.ability_select_state.MultiplayerMenuState'):
        return AbilitySelectState(mock_manager, "SINGLE"), mock_manager


def test_ability_select_state_initialization(ability_state):
    """Test initial state of ability selection."""
    state, _ = ability_state
    assert len(state.options) == 4
    assert state.cursor_index == 0
    assert state.cols > 0


def test_ability_select_state_navigation(ability_state):
    """Test 2D grid navigation logic in the selection menu."""
    state, _ = ability_state
    # Assuming 4 options, cols might be 3 or 2.
    # _calculate_grid_dimensions(16/9) for n=4:
    # sqrt(4 * 1.77) = sqrt(7.11) approx 2.66 -> cols=3.
    # rows = ceil(4/3) = 2.
    state.cols = 3

    # [0 1 2]
    # [3]
    # [Start] (index 4)

    state.cursor_index = 0
    state.on_move_right()
    assert state.cursor_index == 1

    state.on_move_right()
    assert state.cursor_index == 2

    state.on_move_right()
    assert state.cursor_index == 3

    state.on_move_right()
    assert state.cursor_index == 4  # Start button

    state.on_move_right()
    assert state.cursor_index == 0  # Back to first

    state.on_move_down()
    assert state.cursor_index == 3  # Down from 0 is 3 (cols=3)

    state.on_move_down()
    assert state.cursor_index == 4  # Down from 3 is Start


def test_ability_select_state_selection(ability_state):
    """Test selecting and deselecting abilities with a limit of 2."""
    state, _ = ability_state

    # Select first
    state.cursor_index = 0
    state.on_select_option()
    assert state.options[0].is_selected

    # Select second
    state.cursor_index = 1
    state.on_select_option()
    assert state.options[1].is_selected

    # Try select third (limit 2)
    state.cursor_index = 2
    state.on_select_option()
    assert not state.options[2].is_selected

    # Deselect first
    state.cursor_index = 0
    state.on_select_option()
    assert not state.options[0].is_selected

    # Now third should be selectable
    state.cursor_index = 2
    state.on_select_option()
    assert state.options[2].is_selected


def test_ability_select_state_try_start_game(ability_state):
    """Test transitioning to the next state after selecting 2 abilities."""
    state, manager = ability_state
    # Select 2 abilities
    state.options[0].is_selected = True
    state.options[1].is_selected = True

    state.cursor_index = 4  # Start button
    state.on_select_option()

    # Verify events pushed: SET_ABILITIES and GET_ABILITIES (from PlayingState init)
    assert manager.get_event_bus.return_value.push_event.call_count == 2
