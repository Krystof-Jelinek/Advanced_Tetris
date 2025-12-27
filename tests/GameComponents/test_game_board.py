"""
Tests for the GameBoard class.
"""
# pylint: disable=redefined-outer-name, protected-access
import pytest
from src.GameComponents.game_board import GameBoard
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.TetrisSquares.piece_square import PieceSquare


@pytest.fixture
def game_board():
    """Fixture providing a fresh GameBoard instance."""
    return GameBoard()


def test_game_board_initialization(game_board):
    """Test that the game board is initialized with correct dimensions."""
    assert game_board.rows > 0
    assert game_board.cols > 0
    assert len(game_board.grid) == game_board.rows
    assert len(game_board.grid[0]) == game_board.cols


def test_is_valid_move(game_board):
    """Test validation of potential piece positions."""
    # Valid move (center of board)
    assert game_board.is_valid_move([(5, 5)])
    assert game_board.is_valid_move([(game_board.rows, 5)])

    # Invalid move (out of bounds)
    assert game_board.is_valid_move([(-1, 5)]) is False
    assert game_board.is_valid_move([(5, -1)]) is False
    assert game_board.is_valid_move([(5, game_board.cols)]) is False


def test_lock_piece(game_board):
    """Test locking a piece onto the board."""
    piece = TetrisPiece(5, 5, [(0, 1)], (255, 0, 0))
    game_board.lock_piece(piece)

    # Check if squares are now PieceSquares
    assert isinstance(game_board.grid[5][5], PieceSquare)
    assert isinstance(game_board.grid[5][6], PieceSquare)
    assert game_board.grid[5][5].color == (255, 0, 0)


def test_clear_row(game_board):
    """Test clearing a full row and shifting lines down."""
    # Fill a row
    row_to_fill = 0
    for c in range(game_board.cols):
        game_board.grid[row_to_fill][c] = PieceSquare(row_to_fill, c, 0, 0, (255, 255, 255))

    # Fill one square in the row above
    game_board.grid[1][5] = PieceSquare(1, 5, 0, 0, (255, 0, 0))

    game_board.clear_row(row_to_fill)

    assert game_board.grid[0][5].color == (255, 0, 0)
    assert game_board.grid[0][5].grid_row == 0

    # The top row should be empty
    assert game_board.grid[game_board.rows - 1][0].is_empty()
