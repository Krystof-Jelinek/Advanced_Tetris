"""
This module defines the abstract base class for all menu options.
"""
from abc import abstractmethod
from typing import Optional, TYPE_CHECKING

from pyglet.graphics import Batch
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.GameComponents.game_component import GameComponent
from src.GameEngine.GameStates.game_state import GameState
from src.Renderers.GameComponentRenderers.menu_option_renderer import MenuOptionRenderer
from src.Renderers.renderer import Renderer

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class MenuOption(GameComponent):
    """
    Base class representing a selectable option in a menu.
    """
    def __init__(self, text: str):
        """Initializes the menu option with display text."""
        self.text = text
        self.selected = False
        self.background: Optional[BorderedRectangle] = None
        self.label: Optional[Label] = None

    @abstractmethod
    def create_state(self, game_manager: "GameManager") -> "GameState":
        """Creates and returns the next game state associated with this option."""

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the menu option."""
        return MenuOptionRenderer(batch)
