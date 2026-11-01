"""
This module defines the RewindStateRenderer, which draws the game with a rewind overlay on top.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.graphics import Group
from pyglet.shapes import Rectangle
from pyglet.text import Label

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.rewind_state import RewindState


class RewindStateRenderer(Renderer):
    """
    Renderer for the rewind state: the game as usual, plus a tinted board and a REWIND label.
    """
    def render(self, component: "RewindState", offset: Optional[Offset] = None) -> None:
        """Renders the rewound game, then the overlay above the pieces and below the texts."""
        state = component.get_parent_state()
        state.get_renderer(self.batch).render(state, offset)

        corner = state.board[0][0].render_rect
        width = config.board_cols * config.square_size
        height = config.board_rows * config.square_size

        if component.overlay is None:
            component.overlay = Rectangle(
                corner.x, corner.y, width, height,
                color=(80, 140, 255, 70),
                batch=self.batch,
                group=Group(order=15)  # above the pieces (10), below the texts (20)
            )
        else:
            component.overlay.x = corner.x
            component.overlay.y = corner.y

        if component.label is None:
            component.label = Label(
                "<< REWIND",
                font_size=28,
                x=corner.x + width / 2,
                y=corner.y + height / 2,
                anchor_x="center", anchor_y="center",
                color=(255, 255, 255, 255),
                batch=self.batch,
                group=Group(order=20)
            )
        else:
            component.label.x = corner.x + width / 2
            component.label.y = corner.y + height / 2
