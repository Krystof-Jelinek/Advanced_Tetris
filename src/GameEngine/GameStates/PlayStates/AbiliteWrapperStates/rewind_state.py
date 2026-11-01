"""
This module defines the RewindState, which plays the recorded game history backwards.
"""
from typing import TYPE_CHECKING, Optional

from pyglet.graphics import Batch
from pyglet.shapes import Rectangle
from pyglet.text import Label
from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.playing_state_wrapper import PlayingStateWrapper
from src.Renderers.GameStateRenderers.rewind_state_renderer import RewindStateRenderer

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
    from src.GameEngine.GameStates.game_state import GameState
    from src.Renderers.renderer import Renderer

class RewindState(PlayingStateWrapper):
    """
    Wrapper state that restores one memento per frame, newest first, until `seconds` of play are rewound
    (or the history runs out), then hands control back to the wrapped state. Input is ignored meanwhile.
    """
    def __init__(self, wrapped: "PlayingState", seconds: float):
        """Wraps the current state and takes over its history."""
        super().__init__(wrapped)
        self.history = wrapped.get_history()
        self.remaining_steps = round(seconds / self.history.interval)

        #  render objects
        self.overlay: Optional[Rectangle] = None
        self.label: Optional[Label] = None

    def update(self, dt: float, batch: Batch) -> "GameState":
        """Restores the next older memento; returns the wrapped state once the rewind is complete."""
        memento = self.history.pop_latest() if self.remaining_steps > 0 else None
        if memento is None:
            return self._wrapped
        self.remaining_steps -= 1
        self._wrapped.restore(memento)
        return self

    def is_ability_wrappable(self) -> bool:
        """Other abilities cannot wrap a rewind in progress."""
        return False

    # input is ignored while the history is played back
    def on_move_down(self):
        """Ignored during the rewind."""

    def on_move_up(self):
        """Ignored during the rewind."""

    def on_move_left(self):
        """Ignored during the rewind."""

    def on_move_right(self):
        """Ignored during the rewind."""

    def on_hold_piece(self):
        """Ignored during the rewind."""

    def on_use_ability(self, ability_index: int):
        """Ignored during the rewind."""

    def get_parent_state(self) -> "PlayingState":
        """Returns the state being rewound."""
        return self._wrapped

    def can_rewind(self) -> bool:
        """A rewind cannot be started while another one is playing."""
        return False

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer that draws the game with a rewind overlay."""
        return RewindStateRenderer(batch)
