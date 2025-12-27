"""
This module defines the AbilitySelectOptionRenderer for visualising ability choices in the menu.
"""
from typing import Optional, TYPE_CHECKING
from pyglet import shapes

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameEngine.GameStates.Menus.MenuOptions.ability_select_option import AbilitySelectOption


class AbilitySelectOptionRenderer(Renderer):
    """
    Renderer for individual ability cards in the ability selection menu.
    """
    CARD_SIZE = config.ability_image_size
    BORDER_SIZE = 4

    def render(self, component: "AbilitySelectOption", offset: Optional[Offset] = None) -> None:
        """Renders the ability card with highlighting and selection borders."""
        offset = Offset(0, 0).add(offset)
        x = offset.x_offset
        y = offset.y_offset

        border_color = (0, 0, 0)  # Default color (invisible)
        show_border = False

        if component.is_highlighted:
            border_color = (255, 255, 255)
            show_border = True

        if component.is_selected:
            border_color = (0, 255, 0)
            show_border = True

        if component.is_selected and component.is_highlighted:
            border_color = (255, 0, 0)
            show_border = True

        width = config.ability_icon_x  # Šířka/výška karty
        height = config.ability_icon_y
        border = self.BORDER_SIZE  # Šířka rámečku (4px)

        def update_border_piece(rect, px, py, pw, ph):
            """Helper to update or create a border rectangle piece."""
            if rect is None:
                rect = shapes.Rectangle(px, py, pw, ph, color=border_color, batch=self.batch)
            else:
                rect.x = px
                rect.y = py
                rect.width = pw
                rect.height = ph
                rect.color = border_color
                rect.visible = True
            return rect

        if show_border:
            component.border_top = update_border_piece(
                component.border_top, x - border, y + height, width + 2 * border, border
            )

            component.border_bottom = update_border_piece(
                component.border_bottom, x - border, y - border, width + 2 * border, border
            )

            component.border_left = update_border_piece(
                component.border_left, x - border, y, border, height
            )

            component.border_right = update_border_piece(
                component.border_right, x + width, y, border, height
            )

        else:
            if component.border_top:
                component.border_top.visible = False
            if component.border_bottom:
                component.border_bottom.visible = False
            if component.border_left:
                component.border_left.visible = False
            if component.border_right:
                component.border_right.visible = False

        component.ability_instance.get_renderer(self.batch).render(component.ability_instance, offset)
