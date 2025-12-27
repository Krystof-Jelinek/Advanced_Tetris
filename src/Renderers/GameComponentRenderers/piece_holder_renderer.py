"""
This module defines the PieceHolderRenderer for displaying the held Tetris piece.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameComponents.piece_holder import PieceHolder


class PieceHolderRenderer(Renderer):
    """
    Renderer for the piece holder UI element.
    """
    def render(self, component: "PieceHolder", offset: Optional[Offset] = None) -> None:
        """Renders the holder background, label, and the held piece if one exists."""
        offset = offsetProvider.get_piece_holder_offset().add(offset)
        if component.background is None:
            component.background = BorderedRectangle(
                x=offset.x_offset,
                y=offset.y_offset - config.piece_holder_y,
                width=config.piece_holder_x,
                height=config.piece_holder_y,
                color=(50, 50, 50),
                border_color=(255, 255, 255),
                border=2,
                batch=self.batch
            )
        else:
            component.background.x = offset.x_offset
            component.background.y = offset.y_offset - config.piece_holder_y

        if component.label is None:
            component.label = Label(
                text="HOLDING",
                x=offset.x_offset + config.piece_holder_x / 2,
                y=offset.y_offset - config.piece_holder_y/5,
                anchor_x="center", anchor_y="bottom",
                font_size=14,
                color=(255, 255, 255, 255),
                batch=self.batch
            )
        else:
            component.label.x = offset.x_offset + config.piece_holder_x / 2
            component.label.y = offset.y_offset - config.piece_holder_y/5

        if component.piece is not None:
            offset = offset.add(Offset(+config.piece_holder_x/2.5, -config.piece_holder_y/2))
            final_offset = offset.add(component.piece.get_next_piece_hint_offset())
            component.piece.get_renderer(self.batch).render(component.piece, final_offset)
