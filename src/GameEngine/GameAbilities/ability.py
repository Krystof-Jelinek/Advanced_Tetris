"""
This module defines the abstract base class for all game abilities.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from pyglet.graphics import Batch
from pyglet.image import AbstractImage
from pyglet.shapes import BorderedRectangle
from pyglet.sprite import Sprite

from src.GameComponents.game_component import GameComponent
from src.Renderers.GameComponentRenderers.AbilityRenderers.ability_renderer import AbilityRenderer

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
    from src.Renderers.renderer import Renderer


class Ability(GameComponent, ABC):
    """
    Abstract base class for representing a player ability that can be charged and executed.
    """
    def __init__(self, line_price):
        """Initializes the ability with a price in cleared lines."""
        self.usable = False
        self.line_price = line_price

        #  render objects
        self.sprite: Optional[Sprite] = None
        self.background: Optional[BorderedRectangle] = None

    @abstractmethod
    def charge_ability(self, num_of_lines: int):
        """Adds charge to the ability based on the number of lines cleared."""

    def is_usable(self) -> bool:
        """Returns True if the ability is fully charged and ready to use."""
        return self.usable

    def set_usable(self, usable: bool):
        """Sets the usability state of the ability."""
        self.usable = usable

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the ability."""
        return AbilityRenderer(batch)

    @abstractmethod
    def get_icon(self) -> AbstractImage:
        """Return the icon image used to render this ability."""

    @abstractmethod
    def can_execute(self, _game_state: "PlayingState") -> bool:
        """Returns True if the ability can be applied to the game right now (it stays charged otherwise)."""
        return True

    @abstractmethod
    def execute(self, game_state: "PlayingState"):
        """Executes the ability effect on the given game state."""
