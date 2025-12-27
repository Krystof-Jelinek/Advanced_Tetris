"""
Tests for the PieceHolder component.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
from src.GameComponents.piece_holder import PieceHolder
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


def test_piece_holder_initialization():
    """Test initial state of the piece holder."""
    holder = PieceHolder()
    assert holder.is_empty()
    assert not holder._swapped_this_turn


def test_piece_holder_first_swap():
    """Test holding a piece for the first time."""
    holder = PieceHolder()
    piece = MagicMock(spec=TetrisPiece)

    result = holder.swap_piece(piece)

    assert result is None
    assert holder.piece == piece
    piece.null_position_and_visibility.assert_called_once()
    assert holder._swapped_this_turn


def test_piece_holder_second_swap_same_turn():
    """Test that holding piece is only allowed once per turn."""
    holder = PieceHolder()
    piece1 = MagicMock(spec=TetrisPiece)
    piece2 = MagicMock(spec=TetrisPiece)

    holder.swap_piece(piece1)
    result = holder.swap_piece(piece2)

    assert result is None
    assert holder.piece == piece1  # Still piece1
    assert piece2.null_position_and_visibility.call_count == 0


def test_piece_holder_swap_with_held_piece():
    """Test swapping the current piece with an already held piece."""
    holder = PieceHolder()
    held_piece = MagicMock(spec=TetrisPiece)
    new_piece = MagicMock(spec=TetrisPiece)

    # Pre-hold a piece
    holder.piece = held_piece

    result = holder.swap_piece(new_piece)

    assert result == held_piece
    assert holder.piece == new_piece
    new_piece.null_position_and_visibility.assert_called_once()
    held_piece.set_start_position.assert_called_once()


def test_piece_holder_reset_swap():
    """Test resetting the swap lock."""
    holder = PieceHolder()
    piece = MagicMock(spec=TetrisPiece)

    holder.swap_piece(piece)
    assert holder._swapped_this_turn

    holder.reset_swap()
    assert not holder._swapped_this_turn
