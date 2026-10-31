"""
This module defines the RandomPieceGeneratorMemento, a snapshot of the piece bag and the random generator.
"""
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


@dataclass(frozen=True)
class RandomPieceGeneratorMemento:
    """
    Memento: which pieces are left in the bag and where the random sequence is,
    created and read only by RandomPieceGenerator.
    """
    bag: tuple[type["TetrisPiece"], ...]  # piece classes still to be drawn from the current bag
    random_state: tuple  # result of random.Random.getstate(), decides how future bags are shuffled
