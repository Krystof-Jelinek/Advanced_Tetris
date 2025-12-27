"""
This module defines the MenuOptionRenderer for drawing menu buttons.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
if TYPE_CHECKING:
    from src.GameEngine.GameStates.Menus.MenuOptions.menu_option import MenuOption


class MenuOptionRenderer(Renderer):
    """
    Renderer for individual menu options, handling background and labels.
    """
    def render(self, component: "MenuOption", offset: Optional[Offset] = None) -> None:
        """Renders the menu option with appropriate highlighting if selected."""
        if offset is None:
            offset = Offset(0, 0)

        x = offset.x_offset
        y = offset.y_offset
        border_width = 2

        # Draw the background box if not already created
        if component.background is None:
            component.background = BorderedRectangle(
                x=x,
                y=y,
                width=config.menu_option_x,
                height=config.menu_option_y,
                color=(50, 50, 50),
                border_color=(255, 255, 255) if component.selected else (50, 50, 50),
                border=border_width,
                batch=self.batch
            )
        else:
            component.background.x = x
            component.background.y = y
            component.background.border_color = (255, 255, 255) if component.selected else (50, 50, 50)

        # Draw the text label
        if component.label is None:
            component.label = Label(
                text=component.text,
                x=x + config.menu_option_x / 2,
                y=y + config.menu_option_y / 2,
                anchor_x="center",
                anchor_y="center",
                font_size=16,
                color=(255, 255, 255, 255),
                batch=self.batch
            )
        else:
            component.label.text = component.text
            component.label.x = x + config.menu_option_x / 2
            component.label.y = y + config.menu_option_y / 2
