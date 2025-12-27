"""
This module defines the GameOverStateRenderer for drawing the game over screen.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.graphics import Group
from pyglet.text import Label

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.game_over_state import GameOverState


class GameOverStateRenderer(Renderer):
    """
    Renderer for the single-player game over state, showing final score and a message.
    """
    def render(self, component: "GameOverState", offset: Optional[Offset] = None) -> None:
        """Renders the final scoreboard and the 'GAME OVER' text."""
        offset = offsetProvider.get_game_over_offset().add(offset)
        sb_offset = offsetProvider.get_game_over_score_offset()
        component.scoreboard.get_renderer(self.batch).render(component.scoreboard, sb_offset)

        # --- Game Over label ---
        if component.game_over_label is None:
            component.game_over_label = Label(
                "GAME OVER",
                font_name="Arial",
                font_size=48,
                x=offset.x_offset,
                y=offset.y_offset + 50,
                anchor_x="center",
                anchor_y="center",
                color=(255, 255, 255),
                batch=self.batch,
                group=Group(order=20)  # this makes it render on top of everyting
            )
        else:
            component.game_over_label.x = offset.x_offset
            component.game_over_label.y = offset.y_offset + 50
