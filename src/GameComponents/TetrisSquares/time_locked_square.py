"""
This module defines the TimeLockedSquare class, which is a square that can only be cleared after a certain time.
"""
from typing import Tuple

from pyglet.graphics import Batch

from src.GameComponents.TetrisSquares.piece_square import PieceSquare
from src.Renderers.TetrisSquareRenderers.time_locked_square_renderer import TimeLockedSquareRenderer
from src.Renderers.renderer import Renderer


class TimeLockedSquare(PieceSquare):
    """
    A special square used for garbage lines that is temporarily invulnerable to clearing.
    """
    def __init__(self, grid_row: int, grid_col: int, duration: float = 20.0,
                 color: Tuple[int, int, int] = (128, 128, 128)):
        """
        Initializes a TimeLockedSquare, which represents a garbage block that
        cannot be cleared for a certain duration.
        """
        super().__init__(grid_row, grid_col, 0, 0, color)
        self.timer = duration
        self.is_locked = True
        self.render_rect = None

    def update(self, dt: float):
        """
        Updates the square's timer. If the timer expires, the square becomes
        unlocked and its color changes to the 'unlocked_color'.
        """
        if self.is_locked and self.timer > 0:
            self.timer -= dt
            if self.timer <= 0:
                self.timer = 0
                self.is_locked = False

    def is_empty(self) -> bool:
        """Returns False as this square is part of a garbage line."""
        return False

    def is_clearable(self) -> bool:
        """
        Returns True if the square's lock timer has expired.
        """
        return not self.is_locked

    def is_scorable(self) -> bool:
        """Returns False as garbage lines typically don't award points when cleared."""
        return False

    def get_renderer(self, batch: Batch) -> Renderer:
        """Returns the renderer for the time-locked square."""
        # Using GhostSquareRenderer as a placeholder for a distinct visual style
        return TimeLockedSquareRenderer(batch)
