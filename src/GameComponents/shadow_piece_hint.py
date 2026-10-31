"""
This module contains the ShadowPieceHint class which displays where the current piece would land.
"""
from pyglet.graphics import Batch

from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_board import GameBoard
from src.GameComponents.game_component import GameComponent
from src.Renderers.GameComponentRenderers.shadow_piece_hint_renderer import ShadowPieceHintRenderer
from src.Renderers.renderer import Renderer


class ShadowPieceHint(GameComponent):
    """
    Visual component that shows a "ghost" piece at the bottom of the board.
    """
    def __init__(self, piece: "TetrisPiece", game_board: "GameBoard"):
        """Initializes the hint with the current piece and the game board."""
        self.board = game_board
        self.piece = piece
        self.ghost_piece: "TetrisPiece" = piece.clone()

    def set_new_piece(self, new_piece: "TetrisPiece"):
        """Updates the hint to track a new piece."""
        self.piece = new_piece
        self.ghost_piece = new_piece.clone()

    def update_shadow_position(self):
        """Calculates the lowest valid position for the ghost piece."""
        self.ghost_piece = self.piece.clone()
        new_y = 0
        while True:
            wanted_positions = self.piece.get_shifted_positions(-new_y, 0)
            if self.board.is_valid_move(wanted_positions):
                new_y += 1
            else:
                break

        while new_y > 1:
            self.ghost_piece.shift_down()
            new_y -= 1

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Updates the position and returns the renderer for the shadow piece hint."""
        self.update_shadow_position()
        return ShadowPieceHintRenderer(batch)
