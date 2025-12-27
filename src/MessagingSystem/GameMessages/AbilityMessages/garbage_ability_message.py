"""
This module defines the GarbageLinesMessage, which triggers garbage lines on the opponent's board.
"""
from typing import TYPE_CHECKING

from src.MessagingSystem.GameMessages.game_message import register_message, GameMessage

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


@register_message
class GarbageLinesMessage(GameMessage):
    """
    Message sent to add garbage lines to the opponent's game board.
    """
    type: str = "garbage_lines_message"

    @staticmethod
    def create_message() -> "GarbageLinesMessage":
        """Factory method to create a new GarbageLinesMessage."""
        return GarbageLinesMessage()

    def __init__(self):
        """Initializes the garbage lines message."""

    def execute(self, manager: "GameManager"):
        """Adds garbage lines to the current game board if the state supports it."""
        game_state = manager.get_game_state()
        if not game_state.is_ability_wrappable():
            return
        if hasattr(game_state, 'add_garbage_lines'):
            game_state.add_garbage_lines(3, 20.0)
