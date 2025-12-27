"""
Extended tests for TetrisPiece methods.
"""
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


def test_tetris_piece_null_position():
    """Test resetting piece position and visibility."""
    piece = TetrisPiece(5, 5, [(1, 0)], (255, 0, 0))
    piece.null_position_and_visibility()
    assert piece.center_square.grid_row == 0
    assert piece.center_square.grid_col == 0
    assert piece.center_square.render_rect is None


def test_tetris_piece_set_start_position():
    """Test resetting piece to the starting spawn position."""
    piece = TetrisPiece(0, 0, [(1, 0)], (255, 0, 0))
    piece.set_start_position()
    assert piece.center_square.grid_row > 0


def test_get_rotated_positions_ccw():
    """Test calculating rotated positions counter-clockwise."""
    # Center (5,5), relative (1,0) -> Abs (6,5)
    piece = TetrisPiece(5, 5, [(1, 0)], (255, 0, 0))
    # CCW rotation: (dr, dc) -> (dc, -dr)
    # (1, 0) -> (0, -1)
    # Abs: (5, 5) and (5+0, 5-1) = (5, 4)
    positions = piece.get_rotated_positions(clockwise=False)
    assert (5, 5) in positions
    assert (5, 4) in positions


def test_get_shifted_positions():
    """Test calculating shifted positions."""
    piece = TetrisPiece(5, 5, [(1, 0)], (255, 0, 0))
    # shift by (2, 3)
    # original: (5,5), (6,5)
    # shifted: (7,8), (8,8)
    positions = piece.get_shifted_positions(2, 3)
    assert (7, 8) in positions
    assert (8, 8) in positions
