"""
Tests for the ShadowPieceHint component.
"""
from unittest.mock import MagicMock
from src.GameComponents.shadow_piece_hint import ShadowPieceHint
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_board import GameBoard


def test_shadow_piece_hint_initialization():
    """Test initial state of the shadow piece hint."""
    piece = MagicMock(spec=TetrisPiece)
    piece.copy.return_value = MagicMock(spec=TetrisPiece)
    board = MagicMock(spec=GameBoard)

    hint = ShadowPieceHint(piece, board)
    assert hint.piece == piece
    assert hint.board == board
    piece.copy.assert_called_once()


def test_shadow_piece_hint_update_position():
    """Test that the shadow piece position is calculated correctly."""
    piece = MagicMock(spec=TetrisPiece)
    ghost = MagicMock(spec=TetrisPiece)
    piece.copy.return_value = ghost
    board = MagicMock(spec=GameBoard)

    hint = ShadowPieceHint(piece, board)

    # Mock positions for valid move
    # First 2 calls valid, 3rd invalid
    piece.get_shifted_positions.side_effect = [[(1, 1)], [(0, 1)], [(-1, 1)]]
    board.is_valid_move.side_effect = [True, True, False]

    hint.update_shadow_position()

    assert ghost.shift_down.call_count == 1
