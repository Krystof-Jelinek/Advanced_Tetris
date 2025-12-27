"""
This module contains the PieceHolder class which allows players to hold one Tetris piece for later use.
"""
from typing import Optional

from pyglet.graphics import Batch
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_component import GameComponent
from src.Renderers.GameComponentRenderers.piece_holder_renderer import PieceHolderRenderer
from src.Renderers.renderer import Renderer


class PieceHolder(GameComponent):
    """
    Manages the held piece and handles swapping logic.
    """
    def __init__(self):
        """Initializes an empty piece holder."""
        self.piece: Optional[TetrisPiece] = None
        self.background: Optional[BorderedRectangle] = None
        self.label: Optional[Label] = None
        self._swapped_this_turn: bool = False

    def is_empty(self) -> bool:
        """Returns True if no piece is currently held."""
        return self.piece is None

    def swap_piece(self, new_piece: TetrisPiece) -> Optional[TetrisPiece]:
        """
        Swap the held piece with the current active piece.
        Returns the piece to spawn next (either new or held).
        """
        if self._swapped_this_turn:
            return None

        self._swapped_this_turn = True

        if self.piece is None:
            self.piece = new_piece
            self.piece.null_position_and_visibility()
            return None

        old_piece = self.piece
        self.piece = new_piece
        self.piece.null_position_and_visibility()
        old_piece.set_start_position()
        return old_piece

    def reset_swap(self):
        """Resets the swap lock, allowing a new swap in the next turn."""
        self._swapped_this_turn = False

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the piece holder."""
        return PieceHolderRenderer(batch)
