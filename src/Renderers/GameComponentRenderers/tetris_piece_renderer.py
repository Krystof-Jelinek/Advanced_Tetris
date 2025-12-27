"""
This module defines the TetrisPieceRenderer for drawing active pieces.
"""
from typing import TYPE_CHECKING, Optional

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


class TetrisPieceRenderer(Renderer):
    """
    Renderer responsible for drawing all squares that make up a Tetris piece.
    """
    def render(self, component: "TetrisPiece", offset: Optional[Offset] = None) -> None:
        """Iterates through and renders all squares of the Tetris piece."""
        component.center_square.get_renderer(self.batch).render(component.center_square, offset)
        for square in component.relative_squares:
            square.get_renderer(self.batch).render(square, offset)
