"""
This module contains the WaitingForConnectionState for a host waiting for a client to connect.
"""
from typing import Optional
import random

from pyglet.graphics import Batch
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameStates.game_state import GameState
from src.GameEngine.GameStates.PlayStates.multiplayer_playing_state import MultiplayerPlayingState
from src.MessagingSystem.GameMessages.seed_message import SeedMessage
from src.MessagingSystem.LANMessageSystem.lan_messaging_system import LanMessagingSystem
from src.Renderers.GameStateRenderers.waiting_for_connection_renderer import WaitingForConnectionRenderer
from src.Renderers.renderer import Renderer


class WaitingForConnectionState(GameState):
    """
    State representing the wait for an incoming multiplayer connection.
    """
    def __init__(self, messaging_system: "LanMessagingSystem", event_bus: "EventBus",):
        """
        Initializes the state with messaging and event bus references.
        """
        super().__init__()
        self.event_bus = event_bus
        self.messaging_system = messaging_system
        self.background: Optional[BorderedRectangle] = None
        self.label: Optional[Label] = None

    def update(self, dt: float, batch: Batch) -> "GameState":
        """
        Polls for connection and sends the game seed once a client connects.
        """
        if not self.messaging_system.is_running():
            return self
        game_seed = random.randint(0, 9999999)
        self.messaging_system.send_message(SeedMessage.create_message(game_seed))
        self.clear_rendered_objects()
        return MultiplayerPlayingState(self.messaging_system, self.event_bus, game_seed)

    def clear_rendered_objects(self):
        """Clears visual components to release resources."""
        self.background = None
        self.label = None

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the waiting for connection state."""
        return WaitingForConnectionRenderer(batch)
