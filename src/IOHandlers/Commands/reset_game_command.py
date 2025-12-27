"""
This module defines the ResetGameCommand.
"""
from typing import TYPE_CHECKING

from src.IOHandlers.Commands.command import Command

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class ResetGameCommand(Command):
    """
    Command to reset the game.
    """
    def execute(self, game_manager: "GameManager"):
        """Calls the on_reset method on the game manager."""
        game_manager.on_reset()
