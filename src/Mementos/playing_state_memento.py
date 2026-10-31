"""
This module defines the PlayingStateMemento, a snapshot of a whole game in progress.
"""
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Config.difficulty_settings import DifficultySettings
    from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
    from src.Mementos.game_board_memento import GameBoardMemento
    from src.Mementos.piece_holder_memento import PieceHolderMemento
    from src.Mementos.random_piece_generator_memento import RandomPieceGeneratorMemento
    from src.Mementos.score_board_memento import ScoreBoardMemento


@dataclass(frozen=True)
class PlayingStateMemento:
    """
    Memento: the game at one moment, created and read only by PlayingState.

    It is composed of the mementos of the components; the current piece is stored as a clone (Prototype).
    """
    board: "GameBoardMemento"
    current_piece: "TetrisPiece"
    piece_holder: "PieceHolderMemento"
    piece_generator: "RandomPieceGeneratorMemento"
    score_board: "ScoreBoardMemento"
    difficulty: "DifficultySettings"
