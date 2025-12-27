"""
This module defines the BoardSquare class, representing an empty square on the game board.
"""
from typing import Tuple

from pyglet.graphics import Batch

from src.Config.config import config
from src.GameComponents.TetrisSquares.tetris_square import TetrisSquare
from src.Renderers.TetrisSquareRenderers.board_square_renderer import BoardSquareRenderer
from src.Renderers.renderer import Renderer


class BoardSquare(TetrisSquare):
    """
    Represents an empty cell on the Tetris board.
    """
    def __init__(self, grid_row: int, grid_col: int, color: Tuple[int, int, int] = config.board_color):
        """
        Board squares default to a dark gray color unless a specific color is given.
        """
        super().__init__(grid_row, grid_col, color)

    def is_empty(self) -> bool:
        """Returns True as this square is part of the empty board."""
        return True

    def get_renderer(self, batch: Batch) -> Renderer:
        """Returns the renderer for the board square."""
        return BoardSquareRenderer(batch)
