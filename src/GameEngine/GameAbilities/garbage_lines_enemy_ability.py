"""
This module defines the GarbageLinesEnemyAbility class which sends garbage lines to the opponent.
"""
from typing import TYPE_CHECKING

import pyglet
from pyglet.image import AbstractImage

from src.MessagingSystem.GameMessages.AbilityMessages.garbage_ability_message import GarbageLinesMessage
from src.Utils.resource_path import resource_path
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameEvents.events import GameEvent

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class GarbageLinesEnemyAbility(Ability):
    """
    Ability that sends a garbage lines message to the enemy player.
    """
    def charge_ability(self, num_of_lines: int):
        """Charges the ability if lines are cleared."""
        if num_of_lines >= self.line_price:
            self.usable = True

    def __init__(self):
        """Initializes the garbage lines ability with its price."""
        super().__init__(line_price=4)

    def can_execute(self, game_state: "PlayingState") -> bool:
        """Attacks need an opponent who is still playing."""
        return game_state.is_enemy_playing()

    def execute(self, game_state: "PlayingState"):
        """Sends a GarbageLinesMessage through the event bus."""
        event_bus = game_state.get_event_bus()
        event_bus.push_event(GameEvent.SEND_GAME_MESSAGE, GarbageLinesMessage.create_message())

    def get_icon(self) -> AbstractImage:
        """Loads and returns the icon image for this ability."""
        return pyglet.image.load(resource_path("resources/ability_icons/garbage_lines_icon.png"))
