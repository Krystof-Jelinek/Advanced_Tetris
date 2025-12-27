"""
This module defines the TimeLockedSquareRenderer for drawing garbage blocks.
"""
from typing import Optional, TYPE_CHECKING

from pyglet import shapes
from pyglet.graphics import Group

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameComponents.TetrisSquares.piece_square import PieceSquare


class TimeLockedSquareRenderer(Renderer):
    """
    Renderer for time-locked squares, providing a distinct bordered appearance.
    """
    def render(self, component: "PieceSquare", offset: Optional[Offset] = None) -> None:
        """Renders a bordered rectangle for the time-locked square."""
        if component.grid_row + component.relative_row >= config.board_rows:
            component.render_rect = None
            return
        x = (component.grid_col + component.relative_col) * config.square_size + offset.x_offset
        y = (component.grid_row + component.relative_row) * config.square_size + offset.y_offset
        if component.render_rect is None:
            component.render_rect = shapes.BorderedRectangle(
                x=x,
                y=y,
                width=config.square_size,
                height=config.square_size,
                color=component.color,
                border=2,
                border_color=(255, 255, 255),
                batch=self.batch,
                group=Group(order=5)  # this makes it render on top of the board
            )
            component.render_rect.opacity = 255
        else:
            # update pozice a barvy, pokud se změnily
            component.render_rect.x = x
            component.render_rect.y = y
            component.render_rect.color = component.color
            component.render_rect.border_color = (255, 255, 255)
            component.render_rect.opacity = 255
