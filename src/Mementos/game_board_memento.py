"""
This module defines the GameBoardMemento, a snapshot of the squares of a GameBoard.
"""
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameComponents.TetrisSquares.tetris_square import TetrisSquare


@dataclass(frozen=True)
class GameBoardMemento:
    """
    Memento: the board grid at one moment, created and read only by GameBoard.

    The squares are clones (Prototype) that nothing else references, so the snapshot never changes.
    """
    squares: list[list["TetrisSquare"]]
