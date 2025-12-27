"""
This module defines the OPiece (square piece) class.
"""
from src.Config.config import config
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.Utils.offset import Offset


class OPiece(TetrisPiece):
    """
    Square-shaped (O) Tetris piece.
    """
    def __init__(self, center_row: int, center_col: int, color=config.piece_colors["O"]):
        """Initializes the O-piece with its shape and kicks."""
        relative_blocks = [
            (0, 1),
            (1, 0),
            (1, 1),
        ]
        kicks = [(0, 0)]  # OPiece doesnt rotate
        super().__init__(center_row, center_col, relative_blocks, color, kicks)

    # Square piece doesn’t rotate
    def rotate(self, clockwise: bool = True):
        """O-pieces do not rotate."""
        return

    def get_next_piece_hint_offset(self) -> Offset:
        """Returns the rendering offset for the next piece hint."""
        return Offset(-config.next_piece_hint_x/12, -config.next_piece_hint_y/4)
