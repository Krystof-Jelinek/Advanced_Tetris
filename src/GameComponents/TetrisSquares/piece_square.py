"""
This module defines the PieceSquare class, representing a square that belongs to a Tetris piece.
"""
from typing import Tuple

from pyglet.graphics import Batch

from src.GameComponents.TetrisSquares.tetris_square import TetrisSquare
from src.Renderers.TetrisSquareRenderers.piece_square_renderer import PieceSquareRenderer
from src.Renderers.renderer import Renderer


class PieceSquare(TetrisSquare):
    """
    Represents an occupied cell on the board or a cell within a moving piece.
    """
    def __init__(self, grid_row: int, grid_col: int, relative_row: int, relative_col: int, color: Tuple[int, int, int]):
        """Initializes the piece square with grid coordinates and relative position within its piece."""
        super().__init__(grid_row, grid_col, color)
        self.relative_row = relative_row  # relative difference between this square and center square of the piece
        self.relative_col = relative_col

    def is_empty(self) -> bool:
        """Returns False as this square represents part of a piece."""
        return False

    def get_renderer(self, batch: Batch) -> Renderer:
        """Returns the renderer for the piece square."""
        return PieceSquareRenderer(batch)
