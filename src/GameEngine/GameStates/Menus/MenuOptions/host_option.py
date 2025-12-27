"""
This module defines the HostOption class for hosting a multiplayer game.
"""
from typing import TYPE_CHECKING

from src.GameEngine.GameStates.Menus.MenuOptions.menu_option import MenuOption
from src.GameEngine.GameStates.waiting_for_connection_state import WaitingForConnectionState

if TYPE_CHECKING:
    from src.GameEngine.GameStates.game_state import GameState
    from src.GameEngine.game_manager import GameManager


class HostOption(MenuOption):
    """
    Menu option to start the game as a multiplayer host.
    """
    def __init__(self, text: str = "Host"):
        """Initializes the host option with its display text."""
        super().__init__(text)

    def create_state(self, game_manager: "GameManager") -> "GameState":
        """Transitions the game to the waiting for connection state."""
        game_manager.start_multiplayer(True)
        return WaitingForConnectionState(game_manager.get_messaging_system(), game_manager.get_event_bus())
