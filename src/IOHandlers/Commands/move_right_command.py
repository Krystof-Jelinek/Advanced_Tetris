"""
This module defines the MoveRightCommand.
"""
from typing import TYPE_CHECKING

from src.IOHandlers.Commands.command import Command

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class MoveRightCommand(Command):
    """
    Command to move the current piece right.
    """
    def execute(self, game_manager: "GameManager"):
        """Calls the on_move_right method on the game manager."""
        game_manager.on_move_right()
