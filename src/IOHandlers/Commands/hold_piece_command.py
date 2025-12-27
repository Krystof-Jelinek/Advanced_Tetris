"""
This module defines the HoldPieceCommand.
"""
from typing import TYPE_CHECKING

from src.IOHandlers.Commands.command import Command

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class HoldPieceCommand(Command):
    """
    Command to hold the current Tetris piece.
    """
    def execute(self, game_manager: "GameManager"):
        """Calls the on_hold_piece method on the game manager."""
        game_manager.on_hold_piece()
