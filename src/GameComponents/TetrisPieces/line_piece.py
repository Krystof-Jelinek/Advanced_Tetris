"""
This module defines the LinePiece (I-piece) class.
"""
from src.Config.config import config
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.Utils.offset import Offset


class LinePiece(TetrisPiece):
    """
    Line-shaped (I) Tetris piece.
    """
    def __init__(self, center_row: int, center_col: int, color=config.piece_colors["Line"]):
        """Initializes the line piece with its shape and kicks."""
        relative_blocks = [
            (0, -1),
            (0, 1),
            (0, 2),
        ]
        kicks = [(0, 0), (0, -1), (0, 1), (0, -2), (0, 2)]
        super().__init__(center_row, center_col, relative_blocks, color, kicks)

    def get_next_piece_hint_offset(self) -> Offset:
        """Returns the rendering offset for the next piece hint."""
        return Offset(-config.next_piece_hint_x/12, -config.next_piece_hint_y/8)
