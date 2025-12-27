"""
This module defines the multiplayer menu state for hosting or joining a game.
"""
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.GameEngine.GameStates.Menus.MenuOptions.host_option import HostOption
from src.GameEngine.GameStates.Menus.MenuOptions.join_option import JoinOption
from src.GameEngine.GameStates.game_state import GameState
from src.Renderers.GameStateRenderers.multiplayer_menu_state_renderer import MultiplayerMenuStateRenderer
from src.Renderers.renderer import Renderer

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class MultiplayerMenuState(GameState):
    """
    State representing the multiplayer menu for hosting or joining a session.
    """
    def __init__(self, game_manager: "GameManager"):
        """
        Initializes the multiplayer menu with host and join options.
        """
        super().__init__()
        self.game_manager = game_manager
        # pylint: disable=import-outside-toplevel
        from src.GameEngine.GameStates.Menus.MenuOptions.menu_option import MenuOption
        # Menu options for multiplayer
        self.options: list[MenuOption] = [
            HostOption(),
            JoinOption()
        ]
        self.selected_index = 0
        self.next_state = self

        # Extra states
        self.waiting_for_player = False
        self.ip_input_active = False
        self.ip_input = ""

    def update(self, dt: float, batch: Batch) -> GameState:
        """Updates highlighting for options based on selection index."""
        # Highlight the selected option
        for option in self.options:
            option.selected = False
        if not self.waiting_for_player and not self.ip_input_active:
            self.options[self.selected_index].selected = True

        return self.next_state

    def on_move_down(self):
        """Moves selection to the next multiplayer option."""
        if not self.waiting_for_player and not self.ip_input_active:
            self.selected_index = (self.selected_index + 1) % len(self.options)

    def on_move_up(self):
        """Moves selection to the previous multiplayer option."""
        if not self.waiting_for_player and not self.ip_input_active:
            self.selected_index = (self.selected_index - 1) % len(self.options)

    def on_select_option(self):
        """Executes the selected multiplayer option."""
        self.next_state = self.options[self.selected_index].create_state(game_manager=self.game_manager)

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the multiplayer menu state."""
        return MultiplayerMenuStateRenderer(batch)
