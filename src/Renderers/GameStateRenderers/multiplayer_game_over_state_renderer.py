"""
This module defines the MultiplayerGameOverStateRenderer for drawing the match results.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.graphics import Group
from pyglet.text import Label

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider
if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.multiplayer_game_over_state import MultiplayerGameOverState


class MultiplayerGameOverStateRenderer(Renderer):
    """
    Renderer for the multiplayer game over screen, showing win/loss status and both scores.
    """
    def render(self, component: "MultiplayerGameOverState", offset: Optional[Offset] = None) -> None:
        """Renders the win/loss status and final scores for both players."""
        offset = offsetProvider.get_game_over_offset().add(offset)

        # Determine result
        if component.my_score > component.enemy_score:
            result_text = "YOU WON!"
            result_color = (0, 255, 0, 255)
        elif component.my_score < component.enemy_score:
            result_text = "YOU LOST!"
            result_color = (255, 0, 0, 255)
        else:
            result_text = "DRAW!"
            result_color = (255, 255, 0, 255)

        # --- Result label ---
        if component.result_label is None:
            component.result_label = Label(
                result_text,
                font_name="Arial",
                font_size=48,
                x=offset.x_offset,
                y=offset.y_offset + 100,
                anchor_x="center",
                anchor_y="center",
                color=result_color,
                batch=self.batch,
                group=Group(order=20)  # this makes it render on top of everyting

            )
        else:
            component.result_label.text = result_text
            component.result_label.color = result_color
            component.result_label.x = offset.x_offset
            component.result_label.y = offset.y_offset + 100

        # --- Scores ---
        if component.my_score_label is None:
            component.my_score_label = Label(
                f"Your score: {component.my_score}",
                font_name="Arial",
                font_size=28,
                x=offset.x_offset,
                y=offset.y_offset,
                anchor_x="center",
                anchor_y="center",
                color=(255, 255, 255, 255),
                batch=self.batch,
                group=Group(order=20)  # this makes it render on top of everyting
            )
        else:
            component.my_score_label.text = f"Your score: {component.my_score}"
            component.my_score_label.x = offset.x_offset
            component.my_score_label.y = offset.y_offset

        if component.enemy_score_label is None:
            component.enemy_score_label = Label(
                f"Enemy score: {component.enemy_score}",
                font_name="Arial",
                font_size=28,
                x=offset.x_offset,
                y=offset.y_offset - 40,
                anchor_x="center",
                anchor_y="center",
                color=(200, 200, 200, 255),
                batch=self.batch,
                group=Group(order=20)  # this makes it render on top of everyting
            )
        else:
            component.enemy_score_label.text = f"Enemy score: {component.enemy_score}"
            component.enemy_score_label.x = offset.x_offset
            component.enemy_score_label.y = offset.y_offset - 40
