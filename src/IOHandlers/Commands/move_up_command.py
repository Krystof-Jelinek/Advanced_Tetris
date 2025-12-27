"""
This module defines the MoveUpCommand (typically used for rotation).
"""
from typing import TYPE_CHECKING

from src.IOHandlers.Commands.command import Command

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class MoveUpCommand(Command):
    """
    Command to move the current piece up (rotate).
    """
    def execute(self, game_manager: "GameManager"):
        """Calls the on_move_up method on the game manager."""
        game_manager.on_move_up()
