"""
This module defines the AbilityRenderer for drawing individual ability icons.
"""
from typing import Optional, TYPE_CHECKING
from pyglet.shapes import BorderedRectangle
import pyglet

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameEngine.GameAbilities.ability import Ability


class AbilityRenderer(Renderer):
    """
    Renderer for an individual ability icon, including background and visual charging state.
    """
    def render(self, component: "Ability", offset: Optional[Offset] = None) -> None:
        """Renders the ability icon with background and applying opacity based on charge."""
        # Base offset setup (like your other renderers)
        offset = offset or Offset(0, 0)

        if component.background is None:
            component.background = BorderedRectangle(
                x=offset.x_offset,
                y=offset.y_offset,
                width=config.ability_icon_x,
                height=config.ability_icon_y,
                color=(50, 50, 50),
                border_color=(255, 255, 255),
                border=2,
                batch=self.batch
            )
        else:
            component.background.x = offset.x_offset
            component.background.y = offset.y_offset

        # === ICON SPRITE ===
        if component.sprite is None:
            img = component.get_icon()
            component.sprite = pyglet.sprite.Sprite(
                img,
                batch=self.batch
            )
        scale_factor = config.ability_image_size / max(component.sprite.image.width, component.sprite.image.height)
        component.sprite.scale = scale_factor

        # vycentrovat uvnitř backgroundu
        bg_x = component.background.x
        bg_y = component.background.y
        bg_width = component.background.width
        bg_height = component.background.height

        component.sprite.x = bg_x + (bg_width - config.ability_image_size) / 2
        component.sprite.y = bg_y + (bg_height - config.ability_image_size) / 2

        # Apply visual state (usable vs not usable)
        if component.is_usable():
            component.sprite.opacity = 255
            component.sprite.color = (255, 255, 255)
        else:
            component.sprite.opacity = 120
            component.sprite.color = (100, 100, 100)
