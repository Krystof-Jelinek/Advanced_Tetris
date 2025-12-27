"""
This module defines the ScoreBoardRenderer for displaying the player's score.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.graphics import Group
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameComponents.score_board import ScoreBoard


class ScoreBoardRenderer(Renderer):
    """
    Renderer for the scoreboard UI element.
    """
    def render(self, component: "ScoreBoard", offset: Optional[Offset] = None) -> None:
        """Renders the scoreboard background and the current score value."""
        new_offset = offsetProvider.get_scoreboard_offset().add(offset)

        if component.background is None:
            component.background = BorderedRectangle(
                x=new_offset.x_offset,
                y=new_offset.y_offset,
                width=config.score_board_size_x,
                height=config.score_board_size_y,
                color=(30, 30, 30),  # dark gray block
                border_color=(255, 255, 255),  # white border
                border=2,  # thickness in pixels
                batch=self.batch,
                group=Group(order=20)  # this makes it render on top of everyting
            )

        else:
            component.background.x = new_offset.x_offset
            component.background.y = new_offset.y_offset

        if component.title_label is None:
            component.title_label = Label(
                text="SCORE",
                x=new_offset.x_offset + config.score_board_size_x/2,  # center horizontally
                y=new_offset.y_offset + config.score_board_size_y/1.1,
                anchor_x="center", anchor_y="top",
                font_size=12,
                color=(255, 255, 255, 255),
                batch=self.batch,
                group=Group(order=20)  # this makes it render on top of everyting
            )
        else:
            component.title_label.x = new_offset.x_offset + config.score_board_size_x/2
            component.title_label.y = new_offset.y_offset + config.score_board_size_y/1.1

        if component.score_label is None:
            component.score_label = Label(
                text=f"{component.score:05d}",  # zero-padded 5 digits
                x=new_offset.x_offset + config.score_board_size_x/2,
                y=new_offset.y_offset + config.score_board_size_y/1.5,
                anchor_x="center", anchor_y="top",
                font_size=24,
                color=(255, 255, 255, 255),
                batch=self.batch,
                group=Group(order=20)  # this makes it render on top of everyting
            )
        else:
            component.score_label.x = new_offset.x_offset + config.score_board_size_x/2
            component.score_label.y = new_offset.y_offset + config.score_board_size_y/1.5
            component.score_label.text = f"{component.score:05d}"
