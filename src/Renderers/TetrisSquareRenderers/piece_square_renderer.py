"""
This module defines the PieceSquareRenderer for drawing active Tetris piece cells.
"""
from typing import Optional, TYPE_CHECKING

from pyglet import shapes
from pyglet.graphics import Group

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameComponents.TetrisSquares.piece_square import PieceSquare


class PieceSquareRenderer(Renderer):
    """
    Renderer for squares that belong to an active piece or are locked on the board.
    """
    def render(self, component: "PieceSquare", offset: Optional[Offset] = None) -> None:
        """Renders an opaque rectangle for the piece square."""
        if component.grid_row + component.relative_row >= config.board_rows:
            component.render_rect = None
            return
        x = (component.grid_col + component.relative_col) * config.square_size
        y = (component.grid_row + component.relative_row) * config.square_size
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
                group=Group(order=10) # this makes it render on top of the board and shadow piece
            )
        else:
            # update position if it changed
            component.render_rect.x = x
            component.render_rect.y = y
            component.render_rect.color = component.color
