"""
Tests for the RewindState, which plays the recorded history backwards.
"""
# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates.rewind_state import RewindState
from src.Mementos.Caretakers.game_history import GameHistory
from src.Renderers.GameStateRenderers.rewind_state_renderer import RewindStateRenderer


def make_wrapped(memento_count):
    """Returns a mocked game state whose history holds the mementos 1..memento_count (one per 0.05 s)."""
    history = GameHistory(seconds=30.0, interval=0.05)
    originator = MagicMock()
    originator.create_memento.side_effect = range(1, memento_count + 1)
    for _ in range(memento_count):
        history.record(0.05, originator)
    wrapped = MagicMock()
    wrapped.get_history.return_value = history
    return wrapped


def play_to_the_end(rewind_state):
    """Updates the rewind until it hands control back; returns the number of frames and the returned state."""
    frames = 0
    state = rewind_state
    while state is rewind_state:
        state = rewind_state.update(1 / 60, None)
        frames += 1
    return frames, state


def test_restores_newest_first_and_stops_after_the_seconds():
    """10 s at 20 mementos per second = the 200 newest mementos, restored from newest to oldest."""
    wrapped = make_wrapped(600)
    rewind = RewindState(wrapped, seconds=10.0)

    frames, state = play_to_the_end(rewind)

    restored = [call.args[0] for call in wrapped.restore.call_args_list]
    assert restored == list(range(600, 400, -1))
    assert frames == 201  # 200 restores + the frame that hands control back
    assert state is wrapped
    assert len(wrapped.get_history()) == 400  # the rest stays for the next rewind


def test_stops_early_when_history_runs_out():
    """A short game rewinds only as far as its history goes."""
    wrapped = make_wrapped(30)
    _, state = play_to_the_end(RewindState(wrapped, seconds=10.0))
    assert wrapped.restore.call_count == 30
    assert state is wrapped


def test_ignores_input_and_other_abilities():
    """Moves and abilities do nothing while the history plays back."""
    wrapped = make_wrapped(5)
    rewind = RewindState(wrapped, seconds=10.0)
    for action in (rewind.on_move_left, rewind.on_move_right, rewind.on_move_up,
                   rewind.on_move_down, rewind.on_hold_piece):
        action()
    rewind.on_use_ability(0)
    wrapped.on_move_left.assert_not_called()
    wrapped.on_use_ability.assert_not_called()


@pytest.mark.parametrize("question", ["can_rewind", "is_ability_wrappable"])
def test_cannot_be_rewound_or_wrapped_again(question):
    """A rewind in progress cannot start another rewind and cannot be wrapped by other abilities."""
    assert getattr(RewindState(make_wrapped(5), seconds=10.0), question)() is False


def test_uses_the_rewind_renderer():
    """The rewind is drawn with its own renderer (tint + REWIND label)."""
    assert isinstance(RewindState(make_wrapped(5), seconds=10.0).get_renderer(MagicMock()), RewindStateRenderer)
