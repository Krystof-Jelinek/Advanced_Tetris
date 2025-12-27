"""
This module defines the UseAbilityCommand.
"""
from typing import TYPE_CHECKING

from src.IOHandlers.Commands.command import Command

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class UseAbilityCommand(Command):
    """
    Command to trigger a specific player ability.
    """
    def __init__(self, ability_index: int):
        """Initializes the command with the index of the ability to use."""
        self.ability_index = ability_index

    def execute(self, game_manager: "GameManager"):
        """Calls the on_use_ability method on the game manager."""
        game_manager.on_use_ability(ability_index=self.ability_index)
