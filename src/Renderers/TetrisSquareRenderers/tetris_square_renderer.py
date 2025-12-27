"""
This module defines the TetrisSquareRenderer base class.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from pyglet import shapes

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameComponents.TetrisSquares.tetris_square import TetrisSquare


class TetrisSquareRenderer(Renderer):
    """
    Base renderer for all types of squares on the Tetris grid.
    """
    def render(self, component: "TetrisSquare", offset: Optional[Offset] = None) -> None:
        """Renders a simple opaque rectangle for the square."""
        x = component.grid_col * config.square_size
        y = component.grid_row * config.square_size
        if offset is not None:
            x, y = offset.apply_offset(x, y)
        if component.render_rect is None:
            component.render_rect = shapes.Rectangle(
                x,
                y,
                config.square_size,
                config.square_size,
                color=component.color,
                batch=self.batch,
            )
        else:
            # update position if it changed
            component.render_rect.x = x
            component.render_rect.y = y
            component.render_rect.color = component.color
