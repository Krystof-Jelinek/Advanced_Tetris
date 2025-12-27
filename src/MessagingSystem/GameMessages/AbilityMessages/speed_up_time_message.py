"""
This module defines the SpeedUpTimeMessage, which speeds up the game for the opponent.
"""
from typing import TYPE_CHECKING

from src.MessagingSystem.GameMessages.game_message import register_message, GameMessage

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


@register_message
class SpeedUpTimeMessage(GameMessage):
    """
    Message sent to increase the game speed for the opponent for a limited time.
    """
    type: str = "speed_up_time_message"

    @staticmethod
    def create_message() -> "SpeedUpTimeMessage":
        """Factory method to create a new SpeedUpTimeMessage."""
        return SpeedUpTimeMessage()

    def __init__(self):
        """Initializes the speed up time message."""

    def execute(self, manager: "GameManager"):
        """Wraps the opponent's game state with a speed modification effect."""
        game_state = manager.get_game_state()
        if not game_state.is_ability_wrappable():
            return
        # pylint: disable=import-outside-toplevel
        from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.time_speed_modification_state import \
            TimeSpeedModificationState
        new_state = TimeSpeedModificationState(game_state, time=10, power=0.5)
        manager.set_game_state(new_state)
