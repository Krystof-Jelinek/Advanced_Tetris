"""
This module defines the PlayingStateWrapper, a base class for states that wrap and modify the behavior of a PlayingState.
"""
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
from src.Mementos.playing_state_memento import PlayingStateMemento

if TYPE_CHECKING:
    from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
    from src.GameEngine.GameStates.game_state import GameState
    from src.Renderers.renderer import Renderer


class PlayingStateWrapper(PlayingState):
    """
    Base class for wrapping a PlayingState to intercept or modify its logic (e.g., for abilities).
    """
    # pylint: disable=super-init-not-called
    def __init__(self, wrapped: "PlayingState"):
        """Initializes the wrapper with the state it is wrapping."""
        self._wrapped = wrapped

    def get_drop_interval(self) -> float:
        """Forwards the drop interval request to the wrapped state."""
        return self._wrapped.get_drop_interval()

    def update_time_modifier(self, time_modifier_update_value: float):
        """Forwards the time modifier update to the wrapped state."""
        return self._wrapped.update_time_modifier(time_modifier_update_value)

    def update(self, dt: float, batch: Batch) -> "GameState":
        """Forwards the update call to the wrapped state."""
        return self._wrapped.update(dt, batch)

    def move_current_piece_down(self):
        """Forwards the move down action to the wrapped state."""
        return self._wrapped.move_current_piece_down()

    def game_over(self):
        """Forwards the game over call to the wrapped state."""
        return self._wrapped.game_over()

    def eval_piece_drop(self):
        """Forwards the piece drop evaluation to the wrapped state."""
        return self._wrapped.eval_piece_drop()

    def on_move_right(self):
        """Forwards the move right input to the wrapped state."""
        return self._wrapped.on_move_right()

    def on_move_left(self):
        """Forwards the move left input to the wrapped state."""
        return self._wrapped.on_move_left()

    def on_move_up(self):
        """Forwards the move up input to the wrapped state."""
        return self._wrapped.on_move_up()

    def on_move_down(self):
        """Forwards the move down input to the wrapped state."""
        return self._wrapped.on_move_down()

    def on_hold_piece(self):
        """Forwards the hold piece input to the wrapped state."""
        return self._wrapped.on_hold_piece()

    def get_current_piece(self) -> "TetrisPiece":
        """Forwards the current piece request to the wrapped state."""
        return self._wrapped.get_current_piece()

    def set_current_piece(self, new_piece: "TetrisPiece"):
        """Forwards setting the current piece to the wrapped state."""
        return self._wrapped.set_current_piece(new_piece)

    def generate_and_set_new_piece(self):
        """Forwards piece generation and setting to the wrapped state."""
        return self._wrapped.generate_and_set_new_piece()

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Forwards the renderer request to the wrapped state."""
        return self._wrapped.get_renderer(batch)

    def is_ability_wrappable(self) -> bool:
        """Forwards the wrappable check to the wrapped state."""
        return self._wrapped.is_ability_wrappable()

    def create_memento(self) -> "PlayingStateMemento":
        """Forwards memento creation to the wrapped state."""
        return self._wrapped.create_memento()

    def restore(self, memento: "PlayingStateMemento"):
        """Forwards the restore to the wrapped state, so the data lands in the real PlayingState."""
        return self._wrapped.restore(memento)

    def __getattr__(self, name):
        """Forwards attribute access to the wrapped state for any non-overridden attributes."""
        # forward everything other than overriden methods to the wrapped state
        # everything that is directly defined in the PlayingState is forwarded by the playingStateWrapper class
        # everything else we forward here
        # this is here if we wrap another wraper for example or Multiplayergame state
        return getattr(self._wrapped, name)
