"""
This module defines the TimeSpeedModificationState, which modifies the game speed for a limited duration.
"""
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.playing_state_wrapper import PlayingStateWrapper
if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
    from src.GameEngine.GameStates.game_state import GameState


class TimeSpeedModificationState(PlayingStateWrapper):
    """
    Wrapper state that speeds up or slows down the game for a certain amount of time.
    """

    # pylint: disable=super-init-not-called
    def __init__(self, wrapped: "PlayingState", time: int, power: float):
        """
        Initializes the time speed modification state.
        
        for power < 1 it speeds up the game and for power > 1 it slows down the game.
        """
        # intentionally not calling super().__init__()
        # because we are wrapping an existing instance
        self.time = time
        self.power = power
        self.reverse_power: float = 1/power
        self._wrapped = wrapped
        self.remaining_time = time
        self._wrapped.update_time_modifier(power)

    def update(self, dt: float, batch: Batch) -> "GameState":
        """Updates the remaining time for the effect and reverts the speed once finished."""
        new_state = self._wrapped.update(dt, batch)
        if not new_state.is_ability_wrappable():
            return new_state

        self.remaining_time -= dt
        if self.remaining_time <= 0:
            new_state.update_time_modifier(self.reverse_power)
            return new_state
        self._wrapped = new_state  # update wrapped state in case it changed
        return self
