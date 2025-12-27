"""
Tests for the AbilitySystem.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
import pytest
from src.GameEngine.GameAbilities.ability_system import AbilitySystem
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameEvents.events import GameEvent


class MockAbility(Ability):
    """Mock ability for testing purposes."""
    def __init__(self, line_price=10):
        """Initializes the mock ability."""
        super().__init__(line_price)
        self.charge_called_with = 0
        self.execute_called = False

    def charge_ability(self, num_of_lines: int):
        """Tracks charging calls."""
        self.charge_called_with += num_of_lines

    def get_icon(self):
        """Returns None for mock icon."""
        return None

    def execute(self, game_state):
        """Tracks execution state."""
        self.execute_called = True


@pytest.fixture
def ability_system():
    """Fixture providing an AbilitySystem with a mocked game state and event bus."""
    mock_game_state = MagicMock()
    mock_event_bus = MagicMock()
    return AbilitySystem(mock_game_state, mock_event_bus), mock_event_bus


def test_ability_system_subscription(ability_system):
    """Test that the ability system correctly subscribes to events."""
    _system, event_bus = ability_system
    # Check if subscribed to events
    calls = [call[0][0] for call in event_bus.subscribe.call_args_list]
    assert GameEvent.LINES_CLEARED in calls
    assert GameEvent.POST_ABILITIES in calls


def test_resolve_ability(ability_system):
    """Test the resolve_ability logic for usable and unusable states."""
    system, _ = ability_system
    ability = MockAbility()
    # Not usable
    ability.set_usable(False)
    system.resolve_ability(ability)
    assert not ability.execute_called

    # Usable
    ability.set_usable(True)
    system.resolve_ability(ability)
    assert ability.execute_called
    assert not ability.is_usable()  # Should be set to false after execution


def test_on_lines_cleared(ability_system):
    """Test that charging is distributed to active abilities."""
    system, _ = ability_system
    ability1 = MockAbility()
    ability2 = MockAbility()
    system.set_active_abilities([ability1, ability2])

    system.on_lines_cleared({"num_of_rows": 3})

    assert ability1.charge_called_with == 3
    assert ability2.charge_called_with == 3
