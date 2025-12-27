"""
This module defines the AbilitySelectStateRenderer for drawing the ability selection screen.
"""
from typing import Optional, TYPE_CHECKING
import pyglet

from src.Config.config import config
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameEngine.GameStates.Menus.ability_select_state import AbilitySelectState


class AbilitySelectStateRenderer(Renderer):
    """
    Renderer for the ability selection state, handling the grid layout and start button.
    """
    # pylint: disable=too-many-locals
    CARD_WIDTH = config.ability_icon_x
    CARD_HEIGHT = config.ability_icon_y
    H_GAP = 40
    V_GAP = 40

    def render(self, component: "AbilitySelectState", offset: Optional[Offset] = None) -> None:
        """Renders the selection title, the grid of abilities, and the start button."""
        # if offsetProvider.window is None:
        #     return

        screen_center_x = offsetProvider.window.width / 2
        screen_center_y = offsetProvider.window.height * 0.8  # Start from top

        current_y = screen_center_y

        cols = component.cols
        rows = component.rows

        # 1. Title
        if component.title_label is None:
            component.title_label = pyglet.text.Label(
                "Select 2 Abilities",
                font_name='Arial',
                font_size=24,
                anchor_x='center',
                anchor_y='center',
                batch=self.batch
            )
        else:
            component.title_label.batch = self.batch

        component.title_label.x = screen_center_x
        component.title_label.y = current_y

        # Move down after the title
        current_y -= self.CARD_HEIGHT * 1.5   # Adjust for card anchor and padding

        # 2. Render Options (Grid)
        total_grid_width = (cols * self.CARD_WIDTH) + (cols * self.H_GAP)

        start_x = screen_center_x - (total_grid_width / 2)

        for i, option in enumerate(component.options):
            # i = index in the flat list
            r = i // cols
            c = i % cols

            draw_x = start_x + (c * (self.CARD_WIDTH + self.H_GAP))

            draw_y = current_y - (r * (self.CARD_HEIGHT + self.V_GAP))

            option.get_renderer(self.batch).render(option, Offset(draw_x, draw_y))

        # 3. Determine Y position for the Start Button

        if rows > 0:
            start_button_y = current_y - (rows * (self.CARD_HEIGHT + self.V_GAP)) + self.CARD_HEIGHT
        else:
            start_button_y = current_y

        start_button_y -= 50  # Add a final gap before the button

        # 4. Start Button Label
        if component.start_label is None:
            component.start_label = pyglet.text.Label(
                "START GAME",
                font_name='Arial',
                font_size=20,
                anchor_x='center',
                anchor_y='center',
                batch=self.batch
            )
        else:
            component.start_label.batch = self.batch

        # Determine color based on logic
        is_start_highlighted = component.cursor_index == len(component.options)
        selected_count = sum(1 for opt in component.options if opt.is_selected)
        is_ready = selected_count == 2

        if is_ready:
            if is_start_highlighted:
                component.start_label.color = (255, 255, 0, 255)  # Yellow (Ready and Highlighted)
            else:
                component.start_label.color = (0, 255, 0, 255)  # Green (Ready but not Highlighted)
        else:
            if is_start_highlighted:
                component.start_label.color = (150, 150, 100, 255)  # Dim Yellow
            else:
                component.start_label.color = (100, 100, 100, 255)  # Grey

        component.start_label.x = screen_center_x
        component.start_label.y = start_button_y
