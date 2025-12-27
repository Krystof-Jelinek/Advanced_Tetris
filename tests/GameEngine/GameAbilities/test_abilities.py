"""
Tests for individual player abilities.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from src.GameEngine.GameAbilities.bomb_piece_ability import BombPieceAbility
from src.GameEngine.GameAbilities.garbage_lines_enemy_ability import GarbageLinesEnemyAbility
from src.GameEngine.GameAbilities.slow_time_ability import SlowTimeAbility
from src.GameEngine.GameAbilities.speed_up_enemy_time_ability import SpeedUpEnemyTimeAbility
from src.GameEngine.GameEvents.events import GameEvent


@pytest.fixture
def mock_game_state():
    """Fixture providing a mocked game state with a mocked event bus."""
    gs = MagicMock()
    gs.get_event_bus.return_value = MagicMock()
    return gs


def test_bomb_piece_ability_charge_and_execute(mock_game_state):
    """Test charging and executing the BombPieceAbility."""
    ability = BombPieceAbility()
    assert not ability.is_usable()

    ability.charge_ability(2)
    assert not ability.is_usable()

    ability.charge_ability(3)
    assert ability.is_usable()

    ability.execute(mock_game_state)
    mock_game_state.set_current_piece.assert_called_once()


def test_garbage_lines_enemy_ability_execute(mock_game_state):
    """Test executing the GarbageLinesEnemyAbility (pushing network event)."""
    ability = GarbageLinesEnemyAbility()
    ability.execute(mock_game_state)

    bus = mock_game_state.get_event_bus()
    bus.push_event.assert_called_once()
    args = bus.push_event.call_args[0]
    assert args[0] == GameEvent.SEND_GAME_MESSAGE


def test_slow_time_ability_execute(mock_game_state):
    """Test executing the SlowTimeAbility (pushing state change event)."""
    ability = SlowTimeAbility()
    mock_game_state.is_ability_wrappable.return_value = True

    with patch('src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.time_speed_modification_state.TimeSpeedModificationState') as mock_state:
        ability.execute(mock_game_state)
        bus = mock_game_state.get_event_bus()
        bus.push_event.assert_called_once_with(GameEvent.GAME_STATE_CHANGE, mock_state.return_value)


def test_speed_up_enemy_time_ability_execute(mock_game_state):
    """Test executing the SpeedUpEnemyTimeAbility (pushing network event)."""
    ability = SpeedUpEnemyTimeAbility()
    ability.execute(mock_game_state)

    bus = mock_game_state.get_event_bus()
    bus.push_event.assert_called_once()
    args = bus.push_event.call_args[0]
    assert args[0] == GameEvent.SEND_GAME_MESSAGE
