"""
This module defines the ZPiece class.
"""
from src.Config.config import config
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


class ZPiece(TetrisPiece):
    """
    Z-shaped Tetris piece.
    """
    def __init__(self, center_row: int, center_col: int, color=config.piece_colors["Z"]):
        """Initializes the Z-piece with its shape and kicks."""
        relative_blocks = [
            (0, 1),
            (-1, 0),
            (-1, -1),
        ]
        kicks = [(0, 0), (0, -1), (0, 1)]
        super().__init__(center_row, center_col, relative_blocks, color, kicks)
