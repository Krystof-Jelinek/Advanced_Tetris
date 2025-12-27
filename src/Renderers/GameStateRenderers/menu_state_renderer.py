"""
This module defines the MenuStateRenderer for drawing the main menu.
"""
from typing import Optional, TYPE_CHECKING

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameEngine.GameStates.Menus.menu_state import MenuState


class MenuStateRenderer(Renderer):
    """
    Renderer for the main menu, positioning all its selectable options.
    """
    def render(self, component: "MenuState", offset: Optional[Offset] = None) -> None:
        """Renders all menu options with calculated offsets."""
        offset = offsetProvider.get_menu_offset(len(component.options)).add(offset)
        for option in component.options:
            offset = offset.add(Offset(0, -config.menu_option_spacing))
            option.get_renderer(self.batch).render(option, offset)
