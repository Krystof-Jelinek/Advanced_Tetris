# pylint: disable=redefined-outer-name, protected-access
"""
Tests for piece movement actions (MoveDown, MoveLeft, MoveRight).
"""
from unittest.mock import MagicMock
import pytest
from src.GameEngine.GameActions.move_piece_down import MovePieceDown
from src.GameEngine.GameActions.move_piece_left import MovePieceLeft
from src.GameEngine.GameActions.move_piece_right import MovePieceRight


@pytest.fixture
def movement_setup():
    """Fixture providing a mocked piece and board."""
    piece = MagicMock()
    board = MagicMock()
    return piece, board


def test_move_piece_down_valid(movement_setup):
    """Test MovePieceDown when the movement is valid."""
    piece, board = movement_setup
    score_board = MagicMock()
    board.is_valid_move.return_value = True

    action = MovePieceDown(piece, board, score_board)
    action.execute()

    piece.shift_down.assert_called_once()
    score_board.add_soft_drop_score.assert_called_once()


def test_move_piece_down_invalid(movement_setup):
    """Test MovePieceDown when the movement is invalid."""
    piece, board = movement_setup
    score_board = MagicMock()
    board.is_valid_move.return_value = False

    action = MovePieceDown(piece, board, score_board)
    action.execute()

    piece.shift_down.assert_not_called()
    score_board.add_soft_drop_score.assert_not_called()


def test_move_piece_left_valid(movement_setup):
    """Test MovePieceLeft when the movement is valid."""
    piece, board = movement_setup
    board.is_valid_move.return_value = True

    action = MovePieceLeft(piece, board)
    action.execute()

    piece.shift_left.assert_called_once()


def test_move_piece_right_valid(movement_setup):
    """Test MovePieceRight when the movement is valid."""
    piece, board = movement_setup
    board.is_valid_move.return_value = True

    action = MovePieceRight(piece, board)
    action.execute()

    piece.shift_right.assert_called_once()
