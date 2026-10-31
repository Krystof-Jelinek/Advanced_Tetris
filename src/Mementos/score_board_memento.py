"""
This module defines the ScoreBoardMemento, a snapshot of the player's score.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreBoardMemento:
    """
    Memento: the score at one moment, created and read only by ScoreBoard.
    """
    score: int
