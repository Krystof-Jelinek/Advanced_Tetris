"""
This module defines the abstract base class for all game actions.
"""
from abc import ABC, abstractmethod


class GameAction(ABC):
    """
    Abstract base class representing an action that can be performed in the game.
    """
    @abstractmethod
    def execute(self):
        """Executes the action's logic."""
