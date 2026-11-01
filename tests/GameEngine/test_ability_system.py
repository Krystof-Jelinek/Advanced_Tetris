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
    def __init__(self, line_price=10, executable=True):
        """Initializes the mock ability."""
        super().__init__(line_price)
        self.charge_called_with = 0
        self.execute_called_with = None
        self.can_execute_called_with = None
        self.executable = executable

    def charge_ability(self, num_of_lines: int):
        """Tracks charging calls."""
        self.charge_called_with += num_of_lines

    def get_icon(self):
        """Returns None for mock icon."""
        return None

    def can_execute(self, game_state) -> bool:
        """Tracks the state it was asked about and answers with the configured value."""
        self.can_execute_called_with = game_state
        return self.executable

    def execute(self, game_state):
        """Tracks the state it was executed on."""
        self.execute_called_with = game_state


@pytest.fixture
def ability_system():
    """Fixture providing an AbilitySystem with a mocked event bus."""
    mock_event_bus = MagicMock()
    return AbilitySystem(mock_event_bus), mock_event_bus


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
    system.resolve_ability(ability, MagicMock())
    assert ability.execute_called_with is None

    # Usable
    ability.set_usable(True)
    system.resolve_ability(ability, MagicMock())
    assert ability.execute_called_with is not None
    assert not ability.is_usable()  # Should be set to false after execution


def test_resolve_ability_uses_the_given_state(ability_system):
    """The ability is asked about and executed on exactly the state passed in (the current, possibly wrapped one)."""
    system, _ = ability_system
    ability = MockAbility()
    ability.set_usable(True)
    current_state = MagicMock()

    system.resolve_ability(ability, current_state)

    assert ability.can_execute_called_with is current_state
    assert ability.execute_called_with is current_state


def test_resolve_ability_not_executable_stays_charged(ability_system):
    """An ability that cannot be applied right now is not executed and keeps its charge."""
    system, _ = ability_system
    ability = MockAbility(executable=False)
    ability.set_usable(True)

    system.resolve_ability(ability, MagicMock())

    assert ability.execute_called_with is None
    assert ability.is_usable()


def test_on_lines_cleared(ability_system):
    """Test that charging is distributed to active abilities."""
    system, _ = ability_system
    ability1 = MockAbility()
    ability2 = MockAbility()
    system.set_active_abilities([ability1, ability2])

    system.on_lines_cleared({"num_of_rows": 3})

    assert ability1.charge_called_with == 3
    assert ability2.charge_called_with == 3
