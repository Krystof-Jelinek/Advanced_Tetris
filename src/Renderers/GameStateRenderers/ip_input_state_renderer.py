"""
This module defines the IPInputStateRenderer for drawing the IP address input screen.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameEngine.GameStates.ip_input_state import IPInputState


class IPInputStateRenderer(Renderer):
    """
    Renderer for the IP input state, displaying a box and the typed address.
    """
    def render(self, component: "IPInputState", offset: Optional[Offset] = None) -> None:
        """Renders the input box and the current input text."""
        offset = offsetProvider.get_waiting_table_offset().add(offset)

        if component.background is None:
            component.background = BorderedRectangle(
                x=offset.x_offset,
                y=offset.y_offset,
                width=600,
                height=200,
                color=(50, 50, 50),
                border_color=(255, 255, 255),
                border=2,
                batch=self.batch
            )
        else:
            component.background.x = offset.x_offset
            component.background.y = offset.y_offset

        # Draw label
        text_to_display = component.input_text if component.input_text else "Enter server IP:Port"
        if component.label is None:
            component.label = Label(
                text=text_to_display,
                x=offset.x_offset,
                y=offset.y_offset,
                anchor_x="center",
                anchor_y="center",
                font_size=16,
                color=(255, 255, 255, 255),
                multiline=False,
                batch=self.batch
            )
        else:
            component.label.text = text_to_display
            component.label.x = offset.x_offset + 300
            component.label.y = offset.y_offset + 100
