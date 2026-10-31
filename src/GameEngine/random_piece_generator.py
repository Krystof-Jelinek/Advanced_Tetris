"""
This module provides the RandomPieceGenerator class, which handles the randomization of Tetris pieces using a "bag" system to ensure a fair distribution.
"""
import random

from src.Config.config import config
from src.GameComponents.TetrisPieces.j_piece import JPiece
from src.GameComponents.TetrisPieces.l_piece import LPiece
from src.GameComponents.TetrisPieces.line_piece import LinePiece
from src.GameComponents.TetrisPieces.o_piece import OPiece
from src.GameComponents.TetrisPieces.s_piece import SPiece
from src.GameComponents.TetrisPieces.t_piece import TPiece
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.TetrisPieces.z_piece import ZPiece
from src.Mementos.random_piece_generator_memento import RandomPieceGeneratorMemento


class RandomPieceGenerator:
    """
    Generates Tetris pieces randomly using a bag-based shuffling mechanism.
    """
    def __init__(self, seed: int = None):
        """
        Initializes the generator with an optional seed for reproducibility.
        """
        self.random = random.Random(seed)
        self.piece_classes = [TPiece, LPiece, LinePiece, OPiece, JPiece, SPiece, ZPiece]
        self.bag: list[type[TetrisPiece]] = []
        self.refill_bag()

    def refill_bag(self):
        """Shuffle all 7 pieces into a new bag."""
        self.bag = self.piece_classes.copy()
        self.random.shuffle(self.bag)

    def get_next_piece(self) -> TetrisPiece:
        """
        Returns the next piece from the bag, refilling it if empty.
        """
        if not self.bag:
            self.refill_bag()
        piece_class = self.bag.pop()
        return piece_class(center_row=config.board_rows, center_col=int(config.board_cols/2))

    def peek_next_piece_class(self) -> type[TetrisPiece]:
        """
        Returns the class of the next piece without removing it from the bag.
        """
        if not self.bag:
            self.refill_bag()
        return self.bag[-1]

    def peek_next_piece(self) -> TetrisPiece:
        """Return a piece instance for preview without removing it from the bag."""
        piece_class = self.peek_next_piece_class()
        # Use default preview position (you can customize)
        return piece_class(center_row=0, center_col=0)

    def create_memento(self) -> RandomPieceGeneratorMemento:
        """Memento: saves the remaining bag and the state of the random generator."""
        return RandomPieceGeneratorMemento(tuple(self.bag), self.random.getstate())

    def restore(self, memento: RandomPieceGeneratorMemento):
        """Memento: puts the saved bag and random state back, so the same pieces come next again."""
        self.bag = list(memento.bag)
        self.random.setstate(memento.random_state)
