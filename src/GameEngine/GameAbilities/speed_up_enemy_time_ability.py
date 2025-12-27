"""
This module defines the SpeedUpEnemyTimeAbility class which speeds up the opponent's game speed.
"""
from typing import TYPE_CHECKING

import pyglet
from pyglet.image import AbstractImage

from src.Utils.resource_path import resource_path
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameEvents.events import GameEvent
from src.MessagingSystem.GameMessages.AbilityMessages.speed_up_time_message import SpeedUpTimeMessage

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class SpeedUpEnemyTimeAbility(Ability):
    """
    Ability that sends a speed up message to the enemy player.
    """
    def charge_ability(self, num_of_lines: int):
        """Charges the ability if lines are cleared."""
        if num_of_lines >= self.line_price:
            self.usable = True

    def __init__(self):
        """Initializes the speed up enemy time ability with its price."""
        super().__init__(line_price=4)

    def execute(self, game_state: "PlayingState"):
        """Sends a SpeedUpTimeMessage through the event bus."""
        event_bus = game_state.get_event_bus()
        event_bus.push_event(GameEvent.SEND_GAME_MESSAGE, SpeedUpTimeMessage.create_message())

    def get_icon(self) -> AbstractImage:
        """Loads and returns the icon image for this ability."""
        return pyglet.image.load(resource_path("resources/ability_icons/speed_up_time_ability_icon.png"))
