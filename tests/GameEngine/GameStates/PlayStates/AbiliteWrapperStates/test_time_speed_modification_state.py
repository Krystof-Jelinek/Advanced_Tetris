"""
Tests for the TimeSpeedModificationState.
"""
from unittest.mock import MagicMock
from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.time_speed_modification_state import TimeSpeedModificationState


def test_time_speed_modification_state_initialization():
    """Test initial configuration and application of time modifier."""
    mock_wrapped = MagicMock()
    state = TimeSpeedModificationState(mock_wrapped, time=10, power=2.0)

    assert state.time == 10
    assert state.power == 2.0
    assert state.remaining_time == 10
    mock_wrapped.update_time_modifier.assert_called_once_with(2.0)


def test_time_speed_modification_state_update():
    """Test that the state reverts the modifier after the time expires."""
    mock_wrapped = MagicMock()
    mock_wrapped.update.return_value = mock_wrapped
    mock_wrapped.is_ability_wrappable.return_value = True

    state = TimeSpeedModificationState(mock_wrapped, time=1, power=2.0)

    # First update
    result = state.update(0.5, MagicMock())
    assert result == state
    assert state.remaining_time == 0.5

    # Second update triggers finish
    result = state.update(0.6, MagicMock())
    assert result == mock_wrapped
    mock_wrapped.update_time_modifier.assert_any_call(0.5) # reverse_power = 1/2
