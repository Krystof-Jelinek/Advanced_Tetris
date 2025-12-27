"""
This module defines the BoardSquareRenderer for drawing empty board cells.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from pyglet import shapes

from src.Config.config import config
from src.Renderers.TetrisSquareRenderers.tetris_square_renderer import TetrisSquareRenderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameComponents.TetrisSquares.board_square import BoardSquare


class BoardSquareRenderer(TetrisSquareRenderer):
    """
    Renderer for empty board squares, typically drawn with a border.
    """
    def render(self, component: "BoardSquare", offset: Optional[Offset] = None) -> None:
        """Renders the board square as a bordered rectangle at its grid position."""
        size = config.square_size
        border = 2
        x = component.grid_col * size
        y = component.grid_row * size
        if offset is not None:
            x, y = offset.apply_offset(x, y)
        if component.render_rect is None:
            component.render_rect = shapes.BorderedRectangle(
                x, y,
                size, size,
                border=border,
                color=component.color,
                border_color=(255, 255, 255),
                batch=self.batch,
            )
        else:
            component.render_rect.x = x
            component.render_rect.y = y
            component.render_rect.color = component.color
            component.render_rect.border_color = (255, 255, 255)
