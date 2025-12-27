"""
This module defines the SlowTimeAbility class which slows down the player's game speed.
"""
from typing import TYPE_CHECKING

import pyglet
from pyglet.image import AbstractImage

from src.Utils.resource_path import resource_path
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameEvents.events import GameEvent

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class SlowTimeAbility(Ability):
    """
    Ability that slows down the drop interval for a limited time.
    """
    def charge_ability(self, num_of_lines: int):
        """Charges the ability if lines are cleared."""
        if num_of_lines >= self.line_price:
            self.usable = True

    def __init__(self):
        """Initializes the slow time ability with its price."""
        super().__init__(line_price=3)

    def execute(self, game_state: "PlayingState"):
        """Wraps the game state with a TimeSpeedModificationState to slow down time."""
        if not game_state.is_ability_wrappable():
            return
        # pylint: disable=import-outside-toplevel
        from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.time_speed_modification_state import \
            TimeSpeedModificationState
        new_state = TimeSpeedModificationState(game_state, time=10, power=2)
        event_bus = game_state.get_event_bus()
        event_bus.push_event(GameEvent.GAME_STATE_CHANGE, new_state)

    def get_icon(self) -> AbstractImage:
        """Loads and returns the icon image for this ability."""
        return pyglet.image.load(resource_path("resources/ability_icons/slow_time_ability_icon.png"))
