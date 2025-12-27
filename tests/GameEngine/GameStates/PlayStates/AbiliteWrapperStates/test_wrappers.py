"""
Tests for the PlayingStateWrapper base class.
"""
from unittest.mock import MagicMock
from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.playing_state_wrapper import PlayingStateWrapper


def test_playing_state_wrapper_delegation():
    """Test that the wrapper correctly delegates calls and attribute access to the wrapped state."""
    mock_wrapped = MagicMock()
    wrapper = PlayingStateWrapper(mock_wrapped)

    wrapper.get_drop_interval()
    mock_wrapped.get_drop_interval.assert_called_once()

    wrapper.update(0.1, MagicMock())
    mock_wrapped.update.assert_called_once()

    wrapper.on_move_right()
    mock_wrapped.on_move_right.assert_called_once()

    # Test __getattr__
    mock_wrapped.some_custom_method.return_value = "custom"
    assert wrapper.some_custom_method() == "custom"
