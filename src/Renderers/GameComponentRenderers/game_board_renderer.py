"""
This module defines the GameBoardRenderer for drawing the Tetris grid.
"""
from typing import TYPE_CHECKING, Optional

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameComponents.game_board import GameBoard


class GameBoardRenderer(Renderer):
    """
    Renderer responsible for drawing all squares within the game board.
    """
    def render(self, component: "GameBoard", offset: Optional[Offset] = None) -> None:
        """Iterates through and renders all squares on the board."""
        new_offset: Offset = offsetProvider.get_board_offset().add(offset)
        for square in component.iter_squares():
            square.get_renderer(self.batch).render(square, new_offset)
