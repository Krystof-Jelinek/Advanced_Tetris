"""
Tests for the Prototype clone() of squares and pieces.
"""
from unittest.mock import MagicMock
import pytest
from src.GameComponents.TetrisPieces.bomb_piece import BombPiece
from src.GameComponents.TetrisPieces.t_piece import TPiece
from src.GameComponents.TetrisSquares.board_square import BoardSquare
from src.GameComponents.TetrisSquares.piece_square import PieceSquare
from src.GameComponents.TetrisSquares.time_locked_square import TimeLockedSquare


@pytest.mark.parametrize("square", [BoardSquare(3, 4), PieceSquare(3, 4, 1, -1, (255, 0, 0)),
                                    TimeLockedSquare(3, 4, duration=12.5)])
def test_square_clone_is_an_independent_copy_of_the_same_class(square):
    """A clone keeps the class and the data, has no render object and can change without touching the original."""
    shape = MagicMock()
    square.render_rect = shape

    clone = square.clone()

    assert type(clone) is type(square)
    assert (clone.grid_row, clone.grid_col, clone.color) == (square.grid_row, square.grid_col, square.color)
    assert clone.render_rect is None
    assert square.render_rect is shape
    clone.shift_down()
    assert square.grid_row == 3


def test_time_locked_square_clone_keeps_its_own_timer():
    """The lock timer is copied, and ticking the clone does not unlock the original."""
    square = TimeLockedSquare(0, 0, duration=12.5)
    clone = square.clone()
    clone.update(20.0)
    assert not clone.is_locked
    assert square.is_locked and square.timer == 12.5


@pytest.mark.parametrize("piece_cls", [TPiece, BombPiece])
def test_piece_clone_keeps_class_and_shape(piece_cls):
    """A clone of a piece is the same kind of piece in the same position and rotation (a bomb stays a bomb)."""
    piece = piece_cls(10, 4)
    piece.rotate()
    clone = piece.clone()
    assert isinstance(clone, piece_cls)
    assert clone.get_positions() == piece.get_positions()


def test_piece_clone_has_its_own_squares():
    """Moving or rotating the clone does not move the original."""
    piece = TPiece(10, 4)
    clone = piece.clone()
    clone.shift_left()
    clone.rotate()
    assert piece.center_square.grid_col == 4
    assert clone.get_positions() != piece.get_positions()
    assert all(a is not b for a, b in zip(piece.relative_squares, clone.relative_squares))
