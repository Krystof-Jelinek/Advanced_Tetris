"""
Tests for the HoldPiece action.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
import pytest
from src.GameEngine.GameActions.hold_piece import HoldPiece


@pytest.fixture
def hold_setup():
    """Fixture providing components required for the HoldPiece action."""
    holder = MagicMock()
    state = MagicMock()
    shadow = MagicMock()
    next_hint = MagicMock()
    gen = MagicMock()
    return holder, state, shadow, next_hint, gen


def test_hold_piece_execute_empty_holder(hold_setup):
    """Test holding a piece when the holder is currently empty."""
    holder, state, shadow, next_hint, gen = hold_setup
    holder.is_empty.return_value = True

    action = HoldPiece(holder, state, shadow, next_hint, gen)
    action.execute()

    holder.swap_piece.assert_called_once_with(state.current_piece)
    state.generate_and_set_new_piece.assert_called_once()
    shadow.set_new_piece.assert_called_once()
    next_hint.set_piece.assert_called_once()


def test_hold_piece_execute_with_held_piece(hold_setup):
    """Test swapping the current piece with an already held piece."""
    holder, state, shadow, next_hint, gen = hold_setup
    holder.is_empty.return_value = False
    mock_held_piece = MagicMock()
    holder.swap_piece.return_value = mock_held_piece

    action = HoldPiece(holder, state, shadow, next_hint, gen)
    action.execute()

    holder.swap_piece.assert_called_once_with(state.get_current_piece.return_value)
    state.set_current_piece.assert_called_once_with(mock_held_piece)
