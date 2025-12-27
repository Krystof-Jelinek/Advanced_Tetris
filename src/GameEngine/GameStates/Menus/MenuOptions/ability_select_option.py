"""
This module defines the AbilitySelectOption class used in the ability selection menu.
"""
from typing import Type, TYPE_CHECKING
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameStates.Menus.MenuOptions.menu_option import MenuOption

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager
    from src.GameEngine.GameStates.game_state import GameState
    from src.Renderers.renderer import Renderer
    from pyglet.graphics import Batch


class AbilitySelectOption(MenuOption):
    """
    Represents an individual ability option in the selection menu.
    """
    def create_state(self, game_manager: "GameManager") -> "GameState":
        """
        Not used for ability selection options as they toggle state instead of transitioning.
        """

    def __init__(self, ability_cls: Type[Ability]):
        """
        Initializes the option with an ability class and its metadata.
        """
        super().__init__("")
        self.ability_cls = ability_cls
        self.ability_instance = ability_cls()
        self.is_selected = False   # Player has chosen this (part of the 2 selected)
        self.is_highlighted = False

        # Graphics cache (populated by renderer)
        self.border_top = None
        self.border_bottom = None
        self.border_left = None
        self.border_right = None

    def get_renderer(self, batch: "Batch") -> "Renderer":
        """Returns the renderer for the ability selection option."""
        # pylint: disable=import-outside-toplevel
        from src.Renderers.GameComponentRenderers.ability_select_option_renderer import AbilitySelectOptionRenderer
        return AbilitySelectOptionRenderer(batch)
