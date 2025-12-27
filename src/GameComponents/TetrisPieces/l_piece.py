"""
This module defines the LPiece class.
"""
from src.Config.config import config
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.Utils.offset import Offset


class LPiece(TetrisPiece):
    """
    L-shaped Tetris piece.
    """
    def __init__(self, center_row: int, center_col: int, color=config.piece_colors["L"]):
        """Initializes the L-piece with its shape and kicks."""
        relative_blocks = [
            (0, -1),
            (0, 1),
            (+1, +1),
        ]
        kicks = [(0, 0), (0, -1), (0, 1)]
        super().__init__(center_row, center_col, relative_blocks, color, kicks)

    def get_next_piece_hint_offset(self) -> Offset:
        """Returns the rendering offset for the next piece hint."""
        return Offset(0, -config.next_piece_hint_y/5)
