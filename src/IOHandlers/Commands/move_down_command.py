"""
This module defines the MoveDownCommand.
"""
from typing import TYPE_CHECKING

from src.IOHandlers.Commands.command import Command

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class MoveDownCommand(Command):
    """
    Command to move the current piece down.
    """
    def execute(self, game_manager: "GameManager"):
        """Calls the on_move_down method on the game manager."""
        game_manager.on_move_down()
