"""
This module defines the main menu state of the game.
"""
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.GameEngine.GameStates.Menus.MenuOptions.menu_option import MenuOption
from src.GameEngine.GameStates.Menus.MenuOptions.multi_player_option import MultiPlayerOption
from src.GameEngine.GameStates.Menus.MenuOptions.single_player_option import SinglePlayerOption
from src.GameEngine.GameStates.game_state import GameState
from src.Renderers.GameStateRenderers.menu_state_renderer import MenuStateRenderer
from src.Renderers.renderer import Renderer

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class MenuState(GameState):
    """
    State representing the main menu where players choose between game modes.
    """
    def __init__(self, game_manager: "GameManager"):
        """
        Initializes the menu state with available game mode options.
        """
        super().__init__()
        self.options: list[MenuOption] = [SinglePlayerOption(), MultiPlayerOption()]
        self.selected_index = 0
        self.next_state = self
        self.game_manager = game_manager

    def update(self, dt: float, batch: Batch) -> GameState:
        """Updates the selection state of menu options."""
        for option in self.options:
            option.selected = False
        self.options[self.selected_index].selected = True
        return self.next_state

    def on_move_down(self):
        """Moves selection to the next menu option."""
        self.selected_index = (self.selected_index + 1) % len(self.options)

    def on_move_up(self):
        """Moves selection to the previous menu option."""
        self.selected_index = (self.selected_index - 1) % len(self.options)

    def on_select_option(self):
        """Executes the action associated with the selected menu option."""
        self.next_state = self.options[self.selected_index].create_state(self.game_manager)

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the menu state."""
        return MenuStateRenderer(batch)
