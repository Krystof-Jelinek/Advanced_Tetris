"""
This module defines the SinglePlayerOption class for selecting single player mode.
"""
from typing import TYPE_CHECKING

from src.GameEngine.GameStates.Menus.MenuOptions.menu_option import MenuOption

from src.GameEngine.GameStates.Menus.ability_select_state import AbilitySelectState

if TYPE_CHECKING:
    from src.GameEngine.GameStates.game_state import GameState
    from src.GameEngine.game_manager import GameManager


class SinglePlayerOption(MenuOption):
    """
    Menu option to choose the single player game mode.
    """
    def __init__(self, text: str = "Single Player"):
        """Initializes the single player option with its display text."""
        super().__init__(text)

    def create_state(self, game_manager: "GameManager") -> "GameState":
        """Transitions the game to the ability selection state for single player."""
        return AbilitySelectState(game_manager, "SINGLE")
