"""
This module contains the AbilitySystem class which manages the collection of abilities available to the player.
"""
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.GameComponents.game_component import GameComponent
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameEvents.events import GameEvent
from src.Renderers.GameComponentRenderers.AbilityRenderers.ability_system_renderer import AbilitySystemRenderer
from src.Renderers.renderer import Renderer
if TYPE_CHECKING:
    from src.GameEngine.GameEvents.event_bus import EventBus
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class AbilitySystem(GameComponent):
    """
    Manages active abilities, their charging, and execution.
    """
    def __init__(self, event_bus: "EventBus") -> None:
        """Initializes the ability system with game state and event bus subscriptions."""
        self.active_abilities: list[Ability] = []

        # EVENTS
        self.event_bus = event_bus
        self.event_bus.subscribe(GameEvent.LINES_CLEARED, self.on_lines_cleared)
        self.event_bus.subscribe(GameEvent.POST_ABILITIES, self.set_active_abilities)

    def resolve_ability(self, ability: Ability, game_state: "PlayingState"):
        """Executes the given ability if it's usable."""
        if ability.is_usable() and ability.can_execute(game_state):
            ability.execute(game_state)
            ability.set_usable(False)

    def on_lines_cleared(self, data: dict):
        """Charges all active abilities when lines are cleared."""
        num_of_rows = data.get("num_of_rows", 0)
        for ability in self.active_abilities:
            ability.charge_ability(num_of_rows)

    def set_active_abilities(self, abilities: list[Ability]):
        """Sets the list of active abilities."""
        self.active_abilities = abilities

    def add_active_ability(self, ability: Ability):
        """Adds a new active ability to the system."""
        self.active_abilities.append(ability)

    def get_active_abilities(self) -> list[Ability]:
        """Returns the list of currently active abilities."""
        return self.active_abilities

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the ability system."""
        return AbilitySystemRenderer(batch)

    def get_ability(self, ability_index: int) -> Ability:
        """Returns an ability by its index."""
        return self.active_abilities[ability_index]
