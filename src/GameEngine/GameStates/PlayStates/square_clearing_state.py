"""
This module defines the SquareClearingState, which handles the animation and logic for removing full rows.
"""
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.playing_state_wrapper import PlayingStateWrapper
from src.GameEngine.game_manager import GameManager
from src.Renderers.GameStateRenderers.square_clearing_state_renderer import SquareClearingStateRenderer
from src.Renderers.renderer import Renderer

if TYPE_CHECKING:
    from src.GameEngine.GameStates.game_state import GameState
    from src.GameComponents.game_board import GameBoard
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class SquareClearingState(PlayingStateWrapper):
    """
    Temporary state that animates the clearing of squares before returning to play.
    """
    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the square clearing state."""
        return SquareClearingStateRenderer(batch)

    def __init__(self, wrapped: "PlayingState", squares_to_clear: list[tuple[int, int]]):
        """Initializes the clearing state by wrapping the current playing state and identifying squares to clear."""
        super().__init__(wrapped)
        # copy the core context
        self.board = wrapped.board

        # Sorting by row descending is CRITICAL because clearing a square triggers gravity (shifts rows down).
        unique_squares = list(set(squares_to_clear))
        unique_squares.sort(key=lambda x: x[0], reverse=True)
        self.squares_to_clear: list[tuple[int, int]] = unique_squares

        self.timer = 0.0
        self.blink_interval = 0.1
        self.blink_count = 0
        self.max_blinks = 6

    def update(self, dt: float, batch: Batch) -> "GameState":
        """Updates the blink animation and removes squares once animation finishes."""
        self.timer += dt
        if self.timer >= self.blink_interval:
            self.timer = 0.0
            self.blink_count += 1
            # toggle visibility of cleared rows
            for r, c in self.squares_to_clear:
                self.board[r][c].toggle_blink()

            if self.blink_count >= self.max_blinks:
                for r, c in self.squares_to_clear:
                    self.board.clear_square(r, c)
                # swap back to previous playing state
                return self._wrapped
        return self

    def update_enemy_board(self, board: "GameBoard"):
        """Disabled in clearing state."""

    def get_parent_state(self) -> "PlayingState":
        """Returns the wrapped playing state."""
        return self._wrapped

    def on_move_down(self):
        """Disabled in clearing state."""

    def on_move_up(self):
        """Disabled in clearing state."""

    def on_move_left(self):
        """Disabled in clearing state."""

    def on_move_right(self):
        """Disabled in clearing state."""

    def on_hold_piece(self):
        """Disabled in clearing state."""

    def on_select_option(self):
        """Disabled in clearing state."""

    def update_enemy_score(self, new_score: int) -> None:
        """Disabled in clearing state."""

    def on_reset(self, game_manager: "GameManager"):
        """Disabled in clearing state."""

    def on_enemy_ended(self):
        """Disabled in clearing state."""

    def get_drop_interval(self) -> float:
        """Returns the drop interval of the wrapped state."""
        return self._wrapped.get_drop_interval()

    def update_time_modifier(self, time_modifier_update_value: float):
        """Forwards time modifier updates to the wrapped state."""
        return self._wrapped.update_time_modifier(time_modifier_update_value)

    def move_current_piece_down(self):
        """Forwards move down action to the wrapped state."""
        return self._wrapped.move_current_piece_down()

    def game_over(self):
        """Forwards game over action to the wrapped state."""
        return self._wrapped.game_over()

    def eval_piece_drop(self):
        """Forwards piece drop evaluation to the wrapped state."""
        return self._wrapped.eval_piece_drop()
