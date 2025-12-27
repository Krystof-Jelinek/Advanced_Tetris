"""
This module defines the abstract base class GameState for all game states.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.GameComponents.game_component import GameComponent

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class GameState(GameComponent, ABC):
    """
    Abstract base class for representing a specific state of the game.
    """
    def __init__(self):
        """
        Initializes the GameState with itself as the next state.
        """
        self.next_state: "GameState" = self  # stores the next gameState for dynamic state switching

    @abstractmethod
    def update(self, dt: float, batch: Batch) -> "GameState":
        """
        Updates the state logic and returns the state to be used in the next frame.
        """
        raise NotImplementedError()

    def is_ability_wrappable(self) -> bool:
        """
        Returns True if the state can be wrapped by an ability modification state.
        """
        return False

    def on_move_down(self):
        """Handler for the move down input."""

    def on_move_up(self):
        """Handler for the move up input."""

    def on_move_left(self):
        """Handler for the move left input."""

    def on_move_right(self):
        """Handler for the move right input."""

    def on_hold_piece(self):
        """Handler for the hold piece input."""

    def on_select_option(self):
        """Handler for the select/confirm option input."""

    def on_reset(self, game_manager: "GameManager"):
        """Handler for the game reset input."""

    def on_use_ability(self, ability_index: int):
        """Handler for using an ability based on its index."""
