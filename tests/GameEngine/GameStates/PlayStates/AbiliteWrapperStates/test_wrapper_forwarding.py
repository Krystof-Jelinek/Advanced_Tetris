"""
Tests that wrapper states pass questions and restores down to the state they wrap.
"""
# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock, patch
import pytest
from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
from src.GameEngine.GameStates.PlayStates.square_clearing_state import SquareClearingState
from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.playing_state_wrapper import PlayingStateWrapper
from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.time_speed_modification_state import \
    TimeSpeedModificationState


@pytest.fixture
def playing_state():
    """Fixture providing a PlayingState with mocked audio and some recorded history."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_music'):
        state = PlayingState(MagicMock())
    state.history.record(1.0, state)
    return state


def test_playing_state_can_rewind_with_history(playing_state):
    """A playing state with recorded history can be rewound."""
    assert playing_state.can_rewind()


def test_square_clearing_blocks_rewind(playing_state):
    """While rows are being cleared the rewind has to wait."""
    assert not SquareClearingState(playing_state, [(0, 0)]).can_rewind()


def test_can_rewind_is_asked_through_the_whole_chain(playing_state):
    """Slow Time on top of row clearing asks the clearing state, so the answer is still no."""
    chain = TimeSpeedModificationState(SquareClearingState(playing_state, [(0, 0)]), time=10, power=2)
    assert not chain.can_rewind()


def test_single_player_has_no_opponent(playing_state):
    """In single player there is nobody to attack."""
    assert not playing_state.is_enemy_playing()


@pytest.mark.parametrize("enemy_playing", [True, False])
def test_is_enemy_playing_is_forwarded(enemy_playing):
    """A wrapper answers with what the wrapped (e.g. multiplayer) state says."""
    wrapped = MagicMock()
    wrapped.is_enemy_playing.return_value = enemy_playing
    assert PlayingStateWrapper(wrapped).is_enemy_playing() is enemy_playing


def test_restore_through_wrapper_lands_in_the_real_state(playing_state):
    """Restoring through a wrapper changes the real game, not the wrapper."""
    memento = playing_state.create_memento()
    playing_state.difficulty.time_elapsed += 50
    playing_state.score_board.set_score(999)
    wrapper = TimeSpeedModificationState(playing_state, time=10, power=2)

    wrapper.restore(memento)

    assert playing_state.difficulty.time_elapsed == memento.difficulty.time_elapsed
    assert playing_state.score_board.get_score() == 0
    assert "difficulty" not in vars(wrapper)
