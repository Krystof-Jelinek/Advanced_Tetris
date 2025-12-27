"""
This module provides the IPInputState for entering the server's IP address in multiplayer mode.
"""
from typing import Optional

import pyglet
from pyglet.graphics import Batch
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameStates.game_state import GameState
from src.GameEngine.GameStates.PlayStates.multiplayer_playing_state import MultiplayerPlayingState
from src.MessagingSystem.GameMessages.seed_message import SeedMessage
from src.MessagingSystem.LANMessageSystem.lan_messaging_system import LanMessagingSystem
from src.Renderers.GameStateRenderers.ip_input_state_renderer import IPInputStateRenderer
from src.Renderers.renderer import Renderer


class IPInputState(GameState):
    """
    State representing the IP input screen for multiplayer connection.
    """
    def __init__(self, messaging_system: LanMessagingSystem, event_bus: "EventBus"):
        """
        Initializes the IP input state with messaging and event systems.
        """
        super().__init__()
        self.event_bus = event_bus
        self.input_text = ""
        self.messaging_system = messaging_system
        self.background: Optional[BorderedRectangle] = None
        self.label: Optional[Label] = None

    def on_text(self, text):
        """Append characters to the IP input buffer."""
        self.input_text += text  # type characters into buffer

    def on_text_motion(self, motion):
        """Handle text motion events like backspace."""
        if motion == pyglet.window.key.MOTION_BACKSPACE:
            self.input_text = self.input_text[:-1]

    def on_select_option(self):
        """Parses the input text and starts the messaging system."""
        try:
            ip, port = self.input_text.split(":")
            port = int(port)
            self.messaging_system.ip = ip
            self.messaging_system.port = port
            self.messaging_system.start()
        except ValueError:
            pass

    def update(self, dt: float, batch: Batch) -> "GameState":
        """
        Polls for a seed message to transition to the multiplayer playing state.
        """
        if not self.messaging_system.is_running():
            return self
        seed_message = self.messaging_system.receive_message()
        if seed_message is None or not isinstance(seed_message, SeedMessage):
            return self

        game_seed = seed_message.get_seed()
        self.clear_rendered_objects()
        return MultiplayerPlayingState(self.messaging_system, self.event_bus, game_seed)

    def clear_rendered_objects(self):
        """Clears visual components to release resources."""
        self.background = None
        self.label = None

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the IP input state."""
        return IPInputStateRenderer(batch)
