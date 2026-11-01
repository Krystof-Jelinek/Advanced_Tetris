"""
Tests for when each ability can be used (can_execute) and for executing the rewind ability.
"""
# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from src.GameComponents.TetrisPieces.bomb_piece import BombPiece
from src.GameComponents.TetrisPieces.t_piece import TPiece
from src.GameEngine.GameAbilities.bomb_piece_ability import BombPieceAbility
from src.GameEngine.GameAbilities.garbage_lines_enemy_ability import GarbageLinesEnemyAbility
from src.GameEngine.GameAbilities.rewind_time_ability import RewindTimeAbility
from src.GameEngine.GameAbilities.slow_time_ability import SlowTimeAbility
from src.GameEngine.GameAbilities.speed_up_enemy_time_ability import SpeedUpEnemyTimeAbility
from src.GameEngine.GameEvents.events import GameEvent
from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.rewind_state import RewindState
from src.Mementos.Caretakers.game_history import GameHistory


@pytest.fixture
def game_state():
    """Fixture providing a mocked game state."""
    return MagicMock()


@pytest.mark.parametrize("wrappable", [True, False])
def test_slow_time_needs_a_wrappable_state(game_state, wrappable):
    """Slow Time wraps the state, so it can only be used when the state allows it."""
    game_state.is_ability_wrappable.return_value = wrappable
    assert SlowTimeAbility().can_execute(game_state) is wrappable


def test_bomb_on_a_normal_piece(game_state):
    """A normal piece can be turned into a bomb."""
    game_state.get_current_piece.return_value = TPiece(10, 4)
    assert BombPieceAbility().can_execute(game_state)


def test_bomb_not_on_a_bomb(game_state):
    """A bomb cannot be turned into a bomb again (the charge would be wasted)."""
    game_state.get_current_piece.return_value = BombPiece(10, 4)
    assert not BombPieceAbility().can_execute(game_state)


@pytest.mark.parametrize("ability_cls", [GarbageLinesEnemyAbility, SpeedUpEnemyTimeAbility])
@pytest.mark.parametrize("enemy_playing", [True, False])
def test_attacks_need_an_opponent_who_still_plays(game_state, ability_cls, enemy_playing):
    """Attacks are only usable while there is an opponent who is still playing."""
    game_state.is_enemy_playing.return_value = enemy_playing
    assert ability_cls().can_execute(game_state) is enemy_playing


@pytest.mark.parametrize("can_rewind", [True, False])
def test_rewind_asks_the_state(game_state, can_rewind):
    """The rewind is usable exactly when the state says there is something to rewind."""
    game_state.can_rewind.return_value = can_rewind
    assert RewindTimeAbility().can_execute(game_state) is can_rewind


def test_rewind_execute_switches_to_rewind_state_and_announces_it(game_state):
    """Executing the rewind wraps the given state in a RewindState and pushes the TIME_REWIND event (sound)."""
    game_state.get_history.return_value = GameHistory()
    event_bus = game_state.get_event_bus.return_value

    RewindTimeAbility().execute(game_state)

    pushed = [call.args for call in event_bus.push_event.call_args_list]
    new_state = pushed[0][1]
    assert pushed[0][0] == GameEvent.GAME_STATE_CHANGE
    assert isinstance(new_state, RewindState)
    assert new_state.get_parent_state() is game_state
    assert pushed[1] == (GameEvent.TIME_REWIND,)
