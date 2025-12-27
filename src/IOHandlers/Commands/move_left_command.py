"""
This module defines the MoveLeftCommand.
"""
from typing import TYPE_CHECKING

from src.IOHandlers.Commands.command import Command

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class MoveLeftCommand(Command):
    """
    Command to move the current piece left.
    """
    def execute(self, game_manager: "GameManager"):
        """Calls the on_move_left method on the game manager."""
        game_manager.on_move_left()
