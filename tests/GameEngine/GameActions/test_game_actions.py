"""
Tests for rotation game action.
"""
from unittest.mock import MagicMock
from src.GameEngine.GameActions.rotate_piece import RotatePiece
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_board import GameBoard


def test_rotate_piece_success():
    """Test rotating a piece when the destination is valid."""
    # Setup: 3x3 board where rotation is valid
    board = MagicMock(spec=GameBoard)
    board.is_valid_move.return_value = True

    piece = MagicMock(spec=TetrisPiece)
    piece.get_kicks.return_value = [(0, 0)]  # No kicks needed
    piece.get_rotated_positions.return_value = [(1, 1)]  # Mock positions

    action = RotatePiece(piece, board)
    action.execute()

    piece.rotate.assert_called_once()


def test_rotate_piece_fail_invalid_move():
    """Test that rotation is blocked when the destination is invalid."""
    board = MagicMock(spec=GameBoard)
    board.is_valid_move.return_value = False  # Move invalid

    piece = MagicMock(spec=TetrisPiece)
    piece.get_kicks.return_value = [(0, 0)]

    action = RotatePiece(piece, board)
    action.execute()

    piece.rotate.assert_not_called()


def test_rotate_piece_with_kick():
    """Test that rotation applies kicks if the initial rotation fails."""
    board = MagicMock(spec=GameBoard)
    # First kick (0,0) fails, second kick (0, 1) succeeds
    board.is_valid_move.side_effect = [False, True]

    piece = MagicMock(spec=TetrisPiece)
    piece.get_kicks.return_value = [(0, 0), (0, 1)]
    piece.get_rotated_positions.return_value = [(1, 1)]

    action = RotatePiece(piece, board)
    action.execute()

    piece.rotate.assert_called_once()
    # Should have shifted right by 1 (dc=1)
    piece.shift_right.assert_called_once()
    piece.shift_left.assert_not_called()
