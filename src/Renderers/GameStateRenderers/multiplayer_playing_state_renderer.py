"""
This module defines the MultiplayerPlayingStateRenderer for drawing both local and remote game boards.
"""
from typing import Optional, TYPE_CHECKING

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.multiplayer_playing_state import MultiplayerPlayingState


class MultiplayerPlayingStateRenderer(Renderer):
    """
    Renderer for the multiplayer playing state, showing both players' boards side-by-side.
    """
    def render(self, component: "MultiplayerPlayingState", offset: Optional[Offset] = None) -> None:
        """Renders the local game components and the opponent's board and score."""
        default_offset = Offset(-200, 0)
        offset = default_offset.add(offset)
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

        enemy_offset = Offset(600, 0).add(offset)

        component.get_enemy_board().get_renderer(self.batch).render(component.get_enemy_board(), enemy_offset)
        sb = component.get_enemy_score_board()
        sb.get_renderer(self.batch).render(sb, enemy_offset)
