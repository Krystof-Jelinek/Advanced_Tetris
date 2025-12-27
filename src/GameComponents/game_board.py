"""
This module contains the GameBoard class which represents the Tetris grid.
"""
from typing import Iterator

from pyglet.graphics import Batch

from src.Config.config import config
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.TetrisSquares.board_square import BoardSquare
from src.GameComponents.TetrisSquares.piece_square import PieceSquare
from src.GameComponents.TetrisSquares.tetris_square import TetrisSquare
from src.GameComponents.TetrisSquares.time_locked_square import TimeLockedSquare
from src.GameComponents.game_component import GameComponent
from src.Renderers.GameComponentRenderers.game_board_renderer import GameBoardRenderer
from src.Utils.dummy_list import DummyList


class GameBoard(GameComponent):
    """
    Represents the Tetris game grid, managing squares, line clears, and garbage lines.
    """
    def __init__(self):
        """Initializes the game board grid with empty board squares."""
        self.rows = config.board_rows
        self.cols = config.board_cols
        self.grid: list[list[TetrisSquare]] = [
            [BoardSquare(r, c) for c in range(self.cols)]
            for r in range(self.rows)
        ]

    def __getitem__(self, row: int) -> list[TetrisSquare]:
        """Returns the squares of a specific row."""
        if row < 0 or row >= self.rows:
            return DummyList()
        return self.grid[row]

    def iter_squares(self) -> Iterator[TetrisSquare]:
        """Iterate over all squares in row-major order."""
        for row in self.grid:
            yield from row

    def is_valid_move(self, wanted_positions: list[tuple[int, int]]) -> bool:
        """Checks if a set of positions is valid and unoccupied on the board."""
        for row, col in wanted_positions:
            if not (0 <= row and 0 <= col < self.cols):
                return False
            if not row >= self.rows:  # if this is new piece and is generated "above" board
                if not self.grid[row][col].is_empty():
                    return False
        return True

    def lock_piece_possible(self, piece: "TetrisPiece") -> bool:
        """Checks if a piece can be locked at its current position."""
        for row, col in piece.get_positions():
            if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                return False
        return True

    def lock_piece(self, piece: "TetrisPiece"):
        """Place the piece onto the board, marking its squares as occupied."""
        if piece.is_lockable():
            for row, col in piece.get_positions():
                self.grid[row][col] = PieceSquare(row, col, 0, 0, piece.color)

    def clear_row(self, row_idx: int):
        """Remove a row and shift everything above down."""
        # clear the top row
        for c in range(self.cols):
            self.grid[row_idx][c] = BoardSquare(row_idx, c)
        for r in range(row_idx, self.rows - 1, 1):
            for c in range(self.cols):
                self.grid[r][c] = self.grid[r + 1][c]
                self.grid[r][c].shift_down()
        for c in range(self.cols):
            self.grid[self.rows - 1][c] = BoardSquare(self.rows - 1, c)

    def update(self, dt: float):
        """Updates all squares on the board."""
        for row in self.grid:
            for square in row:
                square.update(dt)

    def add_garbage_lines(self, num_lines: int, duration: float = 20.0):
        """
        Adds a specified number of time-locked garbage lines to the bottom of the board,
        shifting existing lines upwards. Lines at the very top of the board will be removed.
        """
        if num_lines <= 0:
            return

        # 1. Shift existing rows upwards
        for r in range(self.rows - 1, num_lines - 1, -1):
            for c in range(self.cols):
                source_square = self.grid[r - num_lines][c]
                if not source_square.is_empty():
                    source_square.grid_row = r
                    self.grid[r][c] = source_square
                else:
                    self.grid[r][c] = BoardSquare(r, c)

        for r in range(num_lines):
            for c in range(self.cols):
                self.grid[r][c] = TimeLockedSquare(r, c, duration=duration)

    def clear_square(self, row_index: int, col_index: int):
        """Remove a square and shift everything above down."""
        self.grid[row_index][col_index] = BoardSquare(row_index, col_index)

        for r in range(row_index, self.rows - 1):
            self.grid[r][col_index] = self.grid[r + 1][col_index]
            if hasattr(self.grid[r][col_index], 'shift_down'):
                self.grid[r][col_index].shift_down()

        self.grid[self.rows - 1][col_index] = BoardSquare(self.rows - 1, col_index)

    def update_board_squares_colors(self, board: "GameBoard"):
        """Updates the colors of board squares to match another board's state."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].color != board[row][col].color:
                    self.grid[row][col].color = board[row][col].color

    def get_renderer(self, batch: Batch) -> "GameBoardRenderer":
        """Returns the renderer for the game board."""
        return GameBoardRenderer(batch)
