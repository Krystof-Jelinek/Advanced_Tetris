"""
This module defines the RewindTimeAbility class which plays the last seconds of the game backwards.
"""
from typing import TYPE_CHECKING

import pyglet
from pyglet.image import AbstractImage

from src.Utils.resource_path import resource_path
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameEvents.events import GameEvent

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class RewindTimeAbility(Ability):
    """
    Ability that rewinds the game to the oldest moment kept in its history and continues from there.
    """
    def charge_ability(self, num_of_lines: int):
        """Charges the ability if lines are cleared."""
        if num_of_lines >= self.line_price:
            self.usable = True

    def __init__(self):
        """Initializes the rewind time ability with its price."""
        super().__init__(line_price=3)

    def can_execute(self, game_state: "PlayingState") -> bool:
        """The rewind needs recorded history and must not start while rows are being cleared."""
        return game_state.can_rewind()

    def execute(self, game_state: "PlayingState"):
        """Wraps the current state with a RewindState that plays the history backwards."""
        # pylint: disable=import-outside-toplevel
        from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.rewind_state import RewindState
        event_bus = game_state.get_event_bus()
        event_bus.push_event(GameEvent.GAME_STATE_CHANGE, RewindState(game_state, seconds=10))
        event_bus.push_event(GameEvent.TIME_REWIND)

    def get_icon(self) -> AbstractImage:
        """Loads and returns the icon image for this ability."""
        return pyglet.image.load(resource_path("resources/ability_icons/time_rewind_ability_icon.png"))
