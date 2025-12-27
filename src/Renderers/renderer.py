"""
This module defines the abstract base class for all renderers in the game.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from pyglet.graphics import Batch

from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameComponents.game_component import GameComponent


class Renderer(ABC):
    """
    Abstract base class for components that handle the visual representation of game objects.
    """
    def __init__(self, batch: Batch):
        """Initializes the renderer with a pyglet graphics batch."""
        self.batch = batch

    @abstractmethod
    def render(self, component: "GameComponent", offset: Optional[Offset] = None) -> None:
        """Renders the given component, optionally applying a translation offset."""
        raise NotImplementedError()
