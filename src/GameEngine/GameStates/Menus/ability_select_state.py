"""
This module contains the AbilitySelectState where players choose their abilities before starting the game.
"""
from typing import List, TYPE_CHECKING
import math

from pyglet.graphics import Batch

from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameAbilities.bomb_piece_ability import BombPieceAbility
from src.GameEngine.GameAbilities.garbage_lines_enemy_ability import GarbageLinesEnemyAbility
from src.GameEngine.GameAbilities.slow_time_ability import SlowTimeAbility
from src.GameEngine.GameAbilities.speed_up_enemy_time_ability import SpeedUpEnemyTimeAbility

from src.GameEngine.GameEvents.events import GameEvent
from src.GameEngine.GameStates.Menus.MenuOptions.ability_select_option import AbilitySelectOption
from src.GameEngine.GameStates.Menus.multiplayer_menu_state import MultiplayerMenuState
from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
from src.GameEngine.GameStates.game_state import GameState
from src.Renderers.GameStateRenderers.ability_select_state_renderer import AbilitySelectStateRenderer
from src.Renderers.renderer import Renderer

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class AbilitySelectState(GameState):
    """
    State representing the ability selection screen.
    """
    def __init__(self, game_manager: "GameManager", game_mode: str):
        """
        Initializes the state with available abilities and layout settings.
        """
        super().__init__()
        self.game_manager = game_manager
        self.game_mode = game_mode

        # Initialize Options
        self.options: List[AbilitySelectOption] = [
            AbilitySelectOption(SlowTimeAbility),
            AbilitySelectOption(SpeedUpEnemyTimeAbility),
            AbilitySelectOption(BombPieceAbility),
            AbilitySelectOption(GarbageLinesEnemyAbility),
        ]

        # Calculate dynamic grid dimensions (Columns, Rows)
        self.cols, self.rows = self._calculate_grid_dimensions()

        self.cursor_index = 0
        self.next_state = self

        # UI Elements Cache
        self.title_label = None
        self.start_label = None

    def _calculate_grid_dimensions(self, target_ar: float = 16.0 / 9.0) -> tuple[int, int]:
        """Calculates the optimal number of columns and rows for a 16:9 aspect ratio."""
        n = len(self.options)

        if n == 0:
            return 1, 0

        # C ≈ sqrt(N * AR)
        optimal_cols_float = math.sqrt(n * target_ar)

        # Use ceil to ensure all items fit and round to the closest integer
        cols = max(1, math.ceil(optimal_cols_float))

        # R = ceil(N / C)
        rows = math.ceil(n / cols)

        return int(cols), int(rows)

    def update(self, dt: float, batch: Batch) -> GameState:
        """Updates highlighting for options based on cursor position."""
        for i, option in enumerate(self.options):
            option.is_highlighted = i == self.cursor_index

        return self.next_state

    #   2D Grid Navigation
    def on_move_right(self):
        """Navigates cursor to the right in the ability grid."""
        max_ability_index = len(self.options) - 1
        start_button_index = len(self.options)

        if self.cursor_index < start_button_index:
            # Moving right through ability grid
            current_col = self.cursor_index % self.cols

            if current_col < self.cols - 1 and self.cursor_index < max_ability_index:
                # Move right normally, staying on the grid and within bounds
                self.cursor_index += 1
            elif self.cursor_index == max_ability_index:
                # If on the very last ability, move to the START button
                self.cursor_index = start_button_index
            else:
                # If at the last column of a row (but not the last ability), wrap to the start of the next row
                # This makes the grid continuous for right/left movement
                next_row_start = self.cursor_index - current_col + self.cols
                if next_row_start <= max_ability_index:
                    self.cursor_index = next_row_start
                else:
                    self.cursor_index = start_button_index
        else:
            self.cursor_index = 0

    def on_move_left(self):
        """Navigates cursor to the left in the ability grid."""
        start_button_index = len(self.options)

        if self.cursor_index < start_button_index:
            # Moving left through ability grid
            current_col = self.cursor_index % self.cols

            if current_col > 0:
                # Move left normally
                self.cursor_index -= 1
            else:
                # If at the first column of a row, wrap to the end of the previous row
                prev_row_end = self.cursor_index - 1
                if prev_row_end >= 0:
                    self.cursor_index = prev_row_end
                else:
                    # If at the first ability (index 0), move to the START button
                    self.cursor_index = start_button_index
        else:
            # If on START button, move to the last ability
            self.cursor_index = len(self.options) - 1 if len(self.options) > 0 else 0

    def on_move_down(self):
        """Navigates cursor down in the ability grid."""
        max_ability_index = len(self.options) - 1
        start_button_index = len(self.options)

        if self.cursor_index < start_button_index:
            # Moving down through ability grid
            new_index = self.cursor_index + self.cols

            if new_index <= max_ability_index:
                # Move down one row normally
                self.cursor_index = new_index
            else:
                # If moving down goes past the last ability, go to the START button
                self.cursor_index = start_button_index
        else:
            # If on the START button, wrap to the first ability
            self.cursor_index = 0

    def on_move_up(self):
        """Navigates cursor up in the ability grid."""
        max_ability_index = len(self.options) - 1
        start_button_index = len(self.options)

        if self.cursor_index < start_button_index:
            # Moving up through ability grid
            new_index = self.cursor_index - self.cols

            if new_index >= 0:
                # Move up one row normally
                self.cursor_index = new_index
            else:
                # If moving up goes past the first row, go to the START button
                self.cursor_index = start_button_index
        else:
            self.cursor_index = max_ability_index if len(self.options) > 0 else 0

    def on_select_option(self):
        """Toggles ability selection or attempts to start the game."""
        start_button_index = len(self.options)

        if self.cursor_index == start_button_index:
            # Try to start
            self.try_start_game()
        else:
            # Toggle Selection
            option = self.options[self.cursor_index]
            if option.is_selected:
                option.is_selected = False
            else:
                # Check limit
                selected_count = sum(1 for opt in self.options if opt.is_selected)
                if selected_count < 2:
                    option.is_selected = True

    def try_start_game(self):
        """Validates selection and transitions to the game or next menu."""
        selected_abilities = [opt.ability_cls for opt in self.options if opt.is_selected]
        if len(selected_abilities) == 2:
            print(f"Starting {self.game_mode} with: {[cls.__name__ for cls in selected_abilities]}")
            active_abilities: list[Ability] = []
            for i in self.options:
                if i.is_selected:
                    active_abilities.append(i.ability_cls())
            event_bus = self.game_manager.get_event_bus()
            event_bus.push_event(GameEvent.SET_ABILITIES, {"abilities": active_abilities})
            if self.game_mode == "SINGLE":
                self.next_state = PlayingState(self.game_manager.get_event_bus())
            if self.game_mode == "MULTI":
                self.next_state = MultiplayerMenuState(self.game_manager)
        else:
            print("Select exactly 2 abilities!")

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the ability selection state."""
        return AbilitySelectStateRenderer(batch)
