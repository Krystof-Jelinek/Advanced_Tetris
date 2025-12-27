"""
This module defines the MultiPlayerOption class for selecting multiplayer mode.
"""
from typing import TYPE_CHECKING

from src.GameEngine.GameStates.Menus.MenuOptions.menu_option import MenuOption
from src.GameEngine.GameStates.Menus.ability_select_state import AbilitySelectState

if TYPE_CHECKING:
    from src.GameEngine.GameStates.game_state import GameState
    from src.GameEngine.game_manager import GameManager


class MultiPlayerOption(MenuOption):
    """
    Menu option to choose the multiplayer game mode.
    """
    def __init__(self, text: str = "Multiplayer"):
        """Initializes the multiplayer option with its display text."""
        super().__init__(text)

    def create_state(self, game_manager: "GameManager") -> "GameState":
        """Transitions the game to the ability selection state for multiplayer."""
        return AbilitySelectState(game_manager, "MULTI")
