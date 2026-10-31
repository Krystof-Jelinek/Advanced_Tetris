"""
This module defines the abstract base class for all Tetris pieces.
"""
import copy
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.Config.config import config
from src.GameComponents.TetrisSquares.piece_square import PieceSquare
from src.GameComponents.game_component import GameComponent
from src.Renderers.renderer import Renderer
from src.Renderers.GameComponentRenderers.tetris_piece_renderer import TetrisPieceRenderer
from src.Utils.offset import Offset
from src.Utils.prototype import Prototype

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class TetrisPiece(GameComponent, Prototype):
    """
    Base class representing a Tetris piece composed of multiple squares.
    """
    def __init__(self, center_row: int, center_col: int, relative_blocks_coordinates: list[tuple[int, int]],
                 color: tuple[int, int, int], kicks: list[tuple[int, int]] = None):
        """Initializes the piece with its center position, relative blocks, color, and kicks."""
        self.center_square: PieceSquare = PieceSquare(center_row, center_col, 0, 0, color)
        self.relative_squares: list[PieceSquare] = [
            PieceSquare(center_row, center_col, dr, dc, color)
            for dr, dc in relative_blocks_coordinates
        ]
        self.color = color
        # used for rotation to make the game more smooth ->
        # if rotation not possible use these to try to find closest possible rotation
        self.kicks: list[tuple[int, int]] = kicks or [(0, 0)]

    def get_kicks(self) -> list[tuple[int, int]]:
        """Returns the rotation kick offsets for the piece."""
        return self.kicks

    def clone(self) -> "TetrisPiece":
        """Prototype: returns an independent copy of this piece with its own squares."""
        piece = copy.copy(self)
        piece.center_square = self.center_square.clone()
        piece.relative_squares = [square.clone() for square in self.relative_squares]
        piece.kicks = list(self.kicks)
        return piece

    # ----------------------------
    # Movement
    # ----------------------------
    def shift_down(self):
        """Moves the entire piece down by one row."""
        self.center_square.grid_row -= 1
        for square in self.relative_squares:
            square.grid_row -= 1

    def shift_left(self):
        """Moves the entire piece left by one column."""
        self.center_square.grid_col -= 1
        for square in self.relative_squares:
            square.grid_col -= 1

    def shift_right(self):
        """Moves the entire piece right by one column."""
        self.center_square.grid_col += 1
        for square in self.relative_squares:
            square.grid_col += 1

    def rotate(self, clockwise: bool = True):
        """Rotate piece 90 degrees around its center square."""
        for square in self.relative_squares:
            if clockwise:
                square.relative_row, square.relative_col = -square.relative_col, square.relative_row
            else:
                square.relative_row, square.relative_col = square.relative_col, -square.relative_row

    def null_position_and_visibility(self):
        """Resets the piece's position to zero and clears its rendered state."""
        self.center_square.grid_row = 0
        self.center_square.grid_col = 0
        self.center_square.clear_rendered()
        for square in self.relative_squares:
            square.grid_row = 0
            square.grid_col = 0
            square.clear_rendered()

    def set_start_position(self):
        """Resets the piece's position to the top-center spawn point."""
        center_row = config.board_rows - 1
        center_col = int(config.board_cols / 2)
        self.center_square.grid_row = center_row
        self.center_square.grid_col = center_col
        for square in self.relative_squares:
            square.grid_row = center_row
            square.grid_col = center_col

    # ----------------------------
    # Validation
    # ----------------------------

    def get_positions(self) -> list[tuple[int, int]]:
        """Return absolute (row, col) positions of all squares occupied by this piece."""
        positions = [(self.center_square.grid_row, self.center_square.grid_col)]
        for sq in self.relative_squares:
            positions.append((sq.grid_row + sq.relative_row, sq.grid_col + sq.relative_col))
        return positions

    def get_shifted_positions(self, d_row: int, d_col: int) -> list[tuple[int, int]]:
        """Return positions if the piece were shifted by (d_row, d_col)."""
        positions = self.get_positions()
        return [(r + d_row, c + d_col) for (r, c) in positions]

    def get_rotated_positions(self, clockwise: bool = True) -> list[tuple[int, int]]:
        """Return positions if the piece were rotated 90° around its center (without modifying it)."""
        positions = [(self.center_square.grid_row, self.center_square.grid_col)]

        for sq in self.relative_squares:
            # simulate rotation of relative coords
            if clockwise:
                rotated_r = -sq.relative_col
                rotated_c = sq.relative_row
            else:
                rotated_r = sq.relative_col
                rotated_c = -sq.relative_row

            # compute absolute positions
            abs_r = self.center_square.grid_row + rotated_r
            abs_c = self.center_square.grid_col + rotated_c
            positions.append((abs_r, abs_c))

        return positions

    # ----------------------------
    # Rendering
    # ----------------------------
    def get_next_piece_hint_offset(self) -> Offset:
        """Returns a custom offset for piece display in the next piece hint."""
        return Offset(0, 0)

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the piece."""
        return TetrisPieceRenderer(batch)

    def on_drop(self, game_state: "PlayingState"):
        """Called when the piece is dropped and locked onto the board."""

    def is_lockable(self) -> bool:
        """Returns True if the piece can be locked into the board grid."""
        return True
