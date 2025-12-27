"""
This module defines the PlayingStateRenderer for drawing the single player gameplay.
"""
from typing import Optional, TYPE_CHECKING

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class PlayingStateRenderer(Renderer):
    """
    Renderer for the single-player playing state, coordinating the rendering of all game components.
    """
    def render(self, component: "PlayingState", offset: Optional[Offset] = None) -> None:
        """Renders the board, active piece, score, and all HUD elements."""
        board = component.board
        board.get_renderer(self.batch).render(board, offset)
        board_offset = offsetProvider.get_board_offset()
        new_offset: Offset = board_offset.add(offset)
        component.current_piece.get_renderer(self.batch).render(component.current_piece, new_offset)
        component.score_board.get_renderer(self.batch).render(component.score_board, offset)
        component.next_piece_hint.get_renderer(self.batch).render(component.next_piece_hint, offset)
        component.piece_holder.get_renderer(self.batch).render(component.piece_holder, offset)
        component.shadow_piece_hint.get_renderer(self.batch).render(component.shadow_piece_hint, offset)
        component.get_ability_system().get_renderer(self.batch).render(component.get_ability_system(), offset)
