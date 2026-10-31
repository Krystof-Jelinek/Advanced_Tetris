"""
This module defines the abstract base class for all squares on the Tetris board.
"""
from abc import abstractmethod
from typing import Tuple
import copy

from pyglet.graphics import Batch
from pyglet.shapes import Rectangle, BorderedRectangle

from src.GameComponents.game_component import GameComponent
from src.Renderers.renderer import Renderer
from src.Renderers.TetrisSquareRenderers.tetris_square_renderer import TetrisSquareRenderer
from src.Utils.prototype import Prototype


class TetrisSquare(GameComponent, Prototype):
    """
    Abstract base class for board and piece squares.
    """
    def __init__(self, grid_row: int, grid_col: int, color: Tuple[int, int, int]):
        """Initializes the square with grid coordinates and color."""
        self.grid_row: int = grid_row
        self.grid_col: int = grid_col
        self.color: Tuple[int, int, int] = color

        # for saving the rendered object
        self.render_rect: Rectangle | BorderedRectangle | None = None

    def get_renderer(self, batch: Batch) -> Renderer:
        """Returns the default renderer for a square."""
        return TetrisSquareRenderer(batch)

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the square is considered empty."""
        raise NotImplementedError

    def get_rendered_object(self) -> Rectangle | BorderedRectangle | None:
        """Returns the underlying pyglet shape used for rendering."""
        return self.render_rect

    def clear_rendered(self):
        """Clears the reference to the rendered pyglet shape."""
        self.render_rect = None

    def shift_down(self):
        """shifts down inner coordinates of square -> used in clearing rows"""
        self.grid_row -= 1

    def toggle_blink(self):
        """Toggles the square's color between white and gray for clearing animation."""
        if self.color == (255, 255, 255):
            self.color = (50, 50, 50)
        else:
            self.color = (255, 255, 255)

    #  this method will be used for time dependant squares
    def update(self, dt: float):
        """Updates the square logic (e.g. for timed effects)."""

    def is_clearable(self) -> bool:
        """
        Returns True if the square can be cleared.
        """
        return True

    def is_scorable(self) -> bool:
        """Returns True if clearing this square contributes to the player's score."""
        return True


    def clone(self) -> "TetrisSquare":
        """Prototype: returns an independent copy of this square (same class) without its render object."""
        square = copy.copy(self)
        square.render_rect = None
        return square
