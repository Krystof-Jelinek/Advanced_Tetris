"""
This module defines the SeedMessage, which synchronizes the random seed between players.
"""
from typing import TYPE_CHECKING

from src.MessagingSystem.GameMessages.game_message import register_message, GameMessage

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


@register_message
class SeedMessage(GameMessage):
    """
    Message sent to synchronize the random piece generation seed at the start of a match.
    """
    type: str = "seed_message"

    @staticmethod
    def create_message(seed: int) -> "SeedMessage":
        """Factory method to create a new SeedMessage with the given seed."""
        return SeedMessage(seed)

    def __init__(self, seed: int):
        """Initializes the seed message with a specific seed value."""
        self.seed = seed

    def execute(self, manager: "GameManager"):
        """No execution logic for seed messages as they are used only for data initialization."""

    def get_seed(self) -> int:
        """Returns the seed contained in the message."""
        return self.seed
