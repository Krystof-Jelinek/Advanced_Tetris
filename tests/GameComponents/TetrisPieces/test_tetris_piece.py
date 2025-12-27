"""
Tests for the base TetrisPiece class functionality.
"""
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


def test_tetris_piece_initialization():
    """Test initializing a generic tetris piece with relative coordinates."""
    # Example piece: 2x1 vertical piece
    # Center at (5, 5), relative (1, 0)
    color = (255, 0, 0)
    relative_coords = [(1, 0)]
    piece = TetrisPiece(5, 5, relative_coords, color)

    assert piece.center_square.grid_row == 5
    assert piece.center_square.grid_col == 5
    assert len(piece.relative_squares) == 1
    assert piece.relative_squares[0].relative_row == 1
    assert piece.relative_squares[0].relative_col == 0
    assert piece.color == color


def test_tetris_piece_movement():
    """Test movement methods (down, left, right)."""
    piece = TetrisPiece(5, 5, [(1, 0)], (255, 0, 0))

    piece.shift_down()
    assert piece.center_square.grid_row == 4
    assert piece.relative_squares[0].grid_row == 4

    piece.shift_left()
    assert piece.center_square.grid_col == 4
    assert piece.relative_squares[0].grid_col == 4

    piece.shift_right()
    assert piece.center_square.grid_col == 5
    assert piece.relative_squares[0].grid_col == 5


def test_tetris_piece_rotation():
    """Test piece rotation logic."""
    # Center at (5, 5), Relative square at (1, 0) -> Absolute (6, 5)
    piece = TetrisPiece(5, 5, [(1, 0)], (255, 0, 0))

    # Clockwise rotation: (dr, dc) -> (-dc, dr)
    # (1, 0) -> (0, 1)
    piece.rotate(clockwise=True)
    assert piece.relative_squares[0].relative_row == 0
    assert piece.relative_squares[0].relative_col == 1

    # Counter-clockwise rotation: (dr, dc) -> (dc, -dr)
    # (0, 1) -> (1, 0)
    piece.rotate(clockwise=False)
    assert piece.relative_squares[0].relative_row == 1
    assert piece.relative_squares[0].relative_col == 0


def test_get_positions():
    """Test calculating absolute positions of all squares in the piece."""
    piece = TetrisPiece(5, 5, [(1, 0)], (255, 0, 0))
    positions = piece.get_positions()
    assert (5, 5) in positions
    assert (6, 5) in positions
    assert len(positions) == 2
