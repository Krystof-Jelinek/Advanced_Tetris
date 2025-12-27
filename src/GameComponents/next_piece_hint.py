"""
This module contains the NextPieceHint class which displays a preview of the next piece.
"""
from typing import Optional

from pyglet.graphics import Batch
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_component import GameComponent
from src.Renderers.GameComponentRenderers.next_piece_hint_renderer import NextPieceHintRenderer
from src.Renderers.renderer import Renderer


class NextPieceHint(GameComponent):
    """
    Visual component that shows the next piece to be spawned.
    """
    def __init__(self, piece: TetrisPiece):
        """Initializes the hint with the next piece."""
        self.piece = piece
        self.background: Optional[BorderedRectangle] = None
        self.label: Optional[Label] = None

    def set_piece(self, piece: TetrisPiece):
        """Updates the preview piece."""
        self.piece = piece

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the next piece hint."""
        return NextPieceHintRenderer(batch)
