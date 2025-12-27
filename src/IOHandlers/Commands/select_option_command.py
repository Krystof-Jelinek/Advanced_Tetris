"""
This module defines the SelectOptionCommand.
"""
from src.GameEngine.game_manager import GameManager
from src.IOHandlers.Commands.command import Command


class SelectOptionCommand(Command):
    """
    Command to select or confirm a menu option.
    """
    def execute(self, game_manager: "GameManager"):
        """Calls the on_select_option method on the game manager."""
        game_manager.on_select_option()
