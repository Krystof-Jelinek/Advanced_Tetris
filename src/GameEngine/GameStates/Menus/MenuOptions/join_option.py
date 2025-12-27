"""
This module defines the JoinOption class for joining a multiplayer game.
"""
from typing import TYPE_CHECKING

from src.GameEngine.GameStates.Menus.MenuOptions.menu_option import MenuOption

from src.GameEngine.GameStates.ip_input_state import IPInputState

if TYPE_CHECKING:
    from src.GameEngine.GameStates.game_state import GameState
    from src.GameEngine.game_manager import GameManager


class JoinOption(MenuOption):
    """
    Menu option to join a multiplayer game as a client.
    """
    def __init__(self, text: str = "Join"):
        """Initializes the join option with its display text."""
        super().__init__(text)

    def create_state(self, game_manager: "GameManager") -> "GameState":
        """Transitions the game to the IP input state."""
        game_manager.start_multiplayer(False)
        return IPInputState(game_manager.get_messaging_system(), game_manager.get_event_bus())
