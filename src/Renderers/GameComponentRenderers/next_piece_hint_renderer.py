"""
This module defines the NextPieceHintRenderer for displaying the next piece preview.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameComponents.next_piece_hint import NextPieceHint


class NextPieceHintRenderer(Renderer):
    """
    Renderer for the next piece hint UI element.
    """
    def render(self, component: "NextPieceHint", offset: Optional[Offset] = None) -> None:
        """Renders the hint background, label, and the next piece itself."""
        offset = offsetProvider.get_next_piece_offset().add(offset)

        # Draw the background box if not already created
        if component.background is None:
            component.background = BorderedRectangle(
                x=offset.x_offset,
                y=offset.y_offset - config.next_piece_hint_y,
                width=config.next_piece_hint_x,
                height=config.next_piece_hint_y,
                color=(50, 50, 50),
                border_color=(255, 255, 255),
                border=2,
                batch=self.batch
            )
        else:
            component.background.x = offset.x_offset
            component.background.y = offset.y_offset - config.next_piece_hint_y

        if component.label is None:
            component.label = Label(
                text="NEXT PIECE",
                x=offset.x_offset + config.next_piece_hint_x / 2,
                y=offset.y_offset - config.next_piece_hint_y/5,
                anchor_x="center", anchor_y="bottom",
                font_size=14,
                color=(255, 255, 255, 255),
                batch=self.batch
            )
        else:
            component.label.x = offset.x_offset + config.next_piece_hint_x / 2
            component.label.y = offset.y_offset - config.next_piece_hint_y/5

        offset = offset.add(Offset(+config.next_piece_hint_x/2.5, -config.next_piece_hint_y/2))
        final_offset = offset.add(component.piece.get_next_piece_hint_offset())
        component.piece.get_renderer(self.batch).render(component.piece, final_offset)
