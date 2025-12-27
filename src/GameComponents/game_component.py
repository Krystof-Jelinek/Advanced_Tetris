"""
This module defines the abstract base class for all game components.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

if TYPE_CHECKING:
    from src.Renderers.renderer import Renderer


class GameComponent(ABC):
    """
    Base class for objects that represent a logical piece of the game and can be rendered.
    """
    @abstractmethod
    def get_renderer(self, batch: Batch) -> "Renderer":
        """
        Return a renderer object that knows how to draw this component.
        also the batch will be given to the renderer
        'renderer' is an object that knows pixel sizes, batches, etc.
        """
        raise NotImplementedError()
