"""
Tests that abilities always act on the state the game is in right now, including wrapper states.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameAbilities.rewind_time_ability import RewindTimeAbility
from src.GameEngine.GameAbilities.slow_time_ability import SlowTimeAbility
from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameEvents.events import GameEvent
from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
from src.GameEngine.GameStates.PlayStates.square_clearing_state import SquareClearingState
from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.time_speed_modification_state import \
    TimeSpeedModificationState


@pytest.fixture
def event_bus():
    """Fixture providing a real event bus, so abilities can really switch the game state."""
    return EventBus()


@pytest.fixture
def playing_state(event_bus):
    """Fixture providing a PlayingState with mocked audio."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_music'):
        return PlayingState(event_bus)


@pytest.fixture
def spy_ability():
    """Fixture providing a mocked, charged ability that records which state it gets."""
    ability = MagicMock(spec=Ability)
    ability.is_usable.return_value = True
    ability.can_execute.return_value = True
    return ability


def follow_state_changes(event_bus):
    """Returns a list that collects every state pushed through GAME_STATE_CHANGE (what GameManager would switch to)."""
    states = []
    event_bus.subscribe(GameEvent.GAME_STATE_CHANGE, states.append)
    return states


def test_ability_gets_the_playing_state_itself(playing_state, spy_ability):
    """Without any wrapper the ability gets the PlayingState."""
    playing_state.ability_system.set_active_abilities([spy_ability])

    playing_state.on_use_ability(0)

    spy_ability.can_execute.assert_called_once_with(playing_state)
    spy_ability.execute.assert_called_once_with(playing_state)


def test_ability_gets_the_wrapper_not_the_inner_state(playing_state, spy_ability):
    """With Slow Time active the ability gets the Slow Time wrapper, which is the state the game is in."""
    playing_state.ability_system.set_active_abilities([spy_ability])
    slow_time = TimeSpeedModificationState(playing_state, time=10, power=2)

    slow_time.on_use_ability(0)

    spy_ability.can_execute.assert_called_once_with(slow_time)
    spy_ability.execute.assert_called_once_with(slow_time)


def test_slow_time_twice_nests_and_both_end(playing_state, event_bus):
    """The second Slow Time wraps the first one, so both restore the speed when they end."""
    first, second = SlowTimeAbility(), SlowTimeAbility()
    playing_state.ability_system.set_active_abilities([first, second])
    states = follow_state_changes(event_bus)

    first.set_usable(True)
    playing_state.on_use_ability(0)
    current = states[-1]
    second.set_usable(True)
    current.on_use_ability(1)
    current = states[-1]

    assert current._wrapped is states[0]  # the second wrapper sits on top of the first
    assert playing_state.time_modifier == 4

    for _ in range(12 * 60):  # 12 s, both effects last 10 s
        current = current.update(1 / 60, None)
    assert current is playing_state
    assert playing_state.time_modifier == 1


def test_rewind_refused_under_slow_time_while_rows_clear(playing_state, event_bus):
    """Slow Time on top of row clearing must still refuse the rewind, and the ability keeps its charge."""
    rewind = RewindTimeAbility()
    playing_state.ability_system.set_active_abilities([rewind])
    playing_state.history.record(1.0, playing_state)  # there is history to rewind
    states = follow_state_changes(event_bus)
    current = TimeSpeedModificationState(SquareClearingState(playing_state, [(0, 0)]), time=10, power=2)

    rewind.set_usable(True)
    current.on_use_ability(0)

    assert not states
    assert rewind.is_usable()
