"""
Tests for all Tetris piece subclasses (J, L, I, O, S, T, Z).
"""
from src.GameComponents.TetrisPieces.j_piece import JPiece
from src.GameComponents.TetrisPieces.l_piece import LPiece
from src.GameComponents.TetrisPieces.line_piece import LinePiece
from src.GameComponents.TetrisPieces.o_piece import OPiece
from src.GameComponents.TetrisPieces.s_piece import SPiece
from src.GameComponents.TetrisPieces.t_piece import TPiece
from src.GameComponents.TetrisPieces.z_piece import ZPiece


def test_all_pieces_initialization():
    """Test that all piece types can be initialized correctly."""
    pieces = [JPiece, LPiece, LinePiece, OPiece, SPiece, TPiece, ZPiece]
    for piece_cls in pieces:
        piece = piece_cls(5, 5)
        assert piece.center_square.grid_row == 5
        assert piece.center_square.grid_col == 5
        assert piece.color is not None
        if not isinstance(piece, OPiece):  # O piece doesn't have kicks usually or different ones
            assert len(piece.get_kicks()) >= 1


def test_piece_offsets():
    """Test that pieces provide offset information for the next piece hint."""
    # Test custom offsets for next piece hint
    p = LinePiece(0, 0)
    offset = p.get_next_piece_hint_offset()
    assert offset is not None
