"""
This module defines the PieceHolderMemento, a snapshot of the held piece and the swap lock.
"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


@dataclass(frozen=True)
class PieceHolderMemento:
    """
    Memento: what the PieceHolder held at one moment, created and read only by PieceHolder.
    """
    held_piece: Optional["TetrisPiece"]  # a clone (Prototype), or None when nothing was held
    swapped_this_turn: bool
