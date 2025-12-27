"""
This module defines the WaitingForConnectionRenderer for drawing the host waiting screen.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.Renderers.renderer import Renderer
from src.Utils.get_local_ip import get_local_ip
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameEngine.GameStates.waiting_for_connection_state import WaitingForConnectionState


class WaitingForConnectionRenderer(Renderer):
    """
    Renderer for the waiting screen, showing local IP and server status.
    """
    def render(self, component: "WaitingForConnectionState", offset: Optional[Offset] = None) -> None:
        """Renders the status box and information about the LAN connection."""
        offset = offsetProvider.get_waiting_table_offset().add(offset)

        ip = get_local_ip()
        port = component.messaging_system.port
        message = f"Your LAN IP: {ip}\nServer listening on {ip}:{port}\nWaiting for player to join..."

        # Draw background box
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
        if component.label is None:
            component.label = Label(
                text=message,
                x=offset.x_offset + 400,
                y=offset.y_offset + 100,
                anchor_x="center",
                anchor_y="center",
                font_size=16,
                color=(255, 255, 255, 255),
                multiline=True,
                width=600,
                batch=self.batch
            )
        else:
            component.label.text = message
            component.label.x = offset.x_offset + 400
            component.label.y = offset.y_offset + 100
