"""
This module defines the abstract base class for all game commands.
"""
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class Command(ABC):
    """
    Abstract base class representing a command that can be executed by the GameManager.
    """
    @abstractmethod
    def execute(self, game_manager: "GameManager"):
        """Executes the command logic using the provided GameManager."""
