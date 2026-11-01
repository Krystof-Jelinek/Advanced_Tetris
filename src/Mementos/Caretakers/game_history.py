"""
This module defines the GameHistory, the caretaker that keeps the recent mementos of a PlayingState.
"""
from collections import deque
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
    from src.Mementos.playing_state_memento import PlayingStateMemento


class GameHistory:
    """
    Caretaker: samples a memento of the game every `interval` seconds and keeps the last `seconds` of them.

    It decides when to save and hands mementos back, but never looks inside them.
    """
    def __init__(self, seconds: float = 30.0, interval: float = 0.05):
        """Creates an empty history; with the defaults it holds 600 mementos (30 s at 20 per second)."""
        self.interval = interval
        self.time_since_record = 0.0
        # a full deque drops its oldest memento on append, which keeps exactly the last `seconds`
        self.mementos: deque["PlayingStateMemento"] = deque(maxlen=round(seconds / interval))

    def record(self, dt: float, originator: "PlayingState"):
        """Asks the originator for a memento once every `interval` seconds of play."""
        self.time_since_record += dt
        if self.time_since_record >= self.interval:
            self.time_since_record -= self.interval
            self.mementos.append(originator.create_memento())

    def pop_latest(self) -> Optional["PlayingStateMemento"]:
        """Removes and returns the newest memento, or None when the history is empty."""
        return self.mementos.pop() if self.mementos else None

    def __len__(self) -> int:
        """Returns the number of stored mementos."""
        return len(self.mementos)
