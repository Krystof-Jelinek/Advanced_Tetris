"""
This module defines the AbilitySystemRenderer for drawing the collection of player abilities.
"""
from typing import Optional, TYPE_CHECKING

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset
from src.Utils.offset_provider import offsetProvider

if TYPE_CHECKING:
    from src.GameEngine.GameAbilities.ability_system import AbilitySystem
    from src.GameEngine.GameAbilities.ability import Ability


class AbilitySystemRenderer(Renderer):
    """
    Renderer responsible for positioning and drawing all active abilities in the ability system.
    """
    def render(self, component: "AbilitySystem", offset: Optional[Offset] = None) -> None:
        """Renders all active abilities with their respective offsets."""
        abilities: list[Ability] = component.get_active_abilities()
        # Defensive: handle if fewer than 2 abilities
        if len(abilities) > 0:
            first_offset = offsetProvider.get_first_ability_offset().add(offset)
            abilities[0].get_renderer(self.batch).render(abilities[0], first_offset)

        if len(abilities) > 1:
            second_offset = offsetProvider.get_second_ability_offset().add(offset)
            abilities[1].get_renderer(self.batch).render(abilities[1], second_offset)
