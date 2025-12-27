"""
This module defines the ShadowPieceHintRenderer for drawing the ghost piece hint.
"""
from typing import Optional, TYPE_CHECKING

from src.Renderers.TetrisSquareRenderers.ghost_square_renderer import GhostSquareRenderer
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameComponents.shadow_piece_hint import ShadowPieceHint


class ShadowPieceHintRenderer(Renderer):
    """
    Renderer for the shadow piece hint, using specialized ghost square rendering.
    """
    def render(self, component: "ShadowPieceHint", offset: Optional[Offset] = None) -> None:
        """Renders the ghost piece at its calculated landing position."""
        new_offset: Offset = offsetProvider.get_board_offset().add(offset)
        renderer = GhostSquareRenderer(self.batch)
        renderer.render(component.ghost_piece.center_square, new_offset)
        for square in component.ghost_piece.relative_squares:
            renderer.render(square, new_offset)
