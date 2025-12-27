"""
Tests for the AbilitySelectOption class.
"""
from unittest.mock import MagicMock
from src.GameEngine.GameStates.Menus.MenuOptions.ability_select_option import AbilitySelectOption
from src.GameEngine.GameAbilities.slow_time_ability import SlowTimeAbility


def test_ability_select_option_initialization():
    """Test initial state of an ability selection option."""
    option = AbilitySelectOption(SlowTimeAbility)
    assert option.ability_cls == SlowTimeAbility
    assert isinstance(option.ability_instance, SlowTimeAbility)
    assert not option.is_selected
    assert not option.is_highlighted


def test_ability_select_option_renderer():
    """Test that the option provides a valid renderer."""
    option = AbilitySelectOption(SlowTimeAbility)
    mock_batch = MagicMock()
    renderer = option.get_renderer(mock_batch)
    assert renderer is not None
