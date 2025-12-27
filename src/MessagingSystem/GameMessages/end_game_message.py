"""
This module defines the EndGameMessage class, used to signal that a player's game has ended.
"""
from typing import TYPE_CHECKING

from src.MessagingSystem.GameMessages.game_message import register_message, GameMessage

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


@register_message
class EndGameMessage(GameMessage):
    """
    Message sent when a player loses or finishes their game.
    """
    type: str = "end_game_message"

    @staticmethod
    def create_message() -> "EndGameMessage":
        """Factory method to create a new EndGameMessage."""
        return EndGameMessage()

    def __init__(self):
        """Initializes the end game message."""

    def execute(self, manager: "GameManager"):
        """Signals the opponent that this player has finished."""
        print("executing end_game_message")
        manager.get_game_state().on_enemy_ended()
