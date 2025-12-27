"""
This module defines the RotatePiece action for rotating the current Tetris piece.
"""
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_board import GameBoard
from src.GameEngine.GameActions.game_action import GameAction


class RotatePiece(GameAction):
    """
    Action that rotates the current piece, applying wall kicks if necessary.
    """
    def __init__(self, piece: TetrisPiece, board: GameBoard):
        """Initializes the action with piece and board."""
        self.piece = piece
        self.board = board

    def execute(self):
        """Attempts to rotate the piece, trying different wall kick offsets."""
        kicks = self.piece.get_kicks()
        for _, dc in kicks:
            positions = self.piece.get_rotated_positions()
            positions = [(r, c + dc) for r, c in positions]
            if self.board.is_valid_move(positions):
                if dc > 0:
                    for _ in range(dc):
                        self.piece.shift_right()
                if dc < 0:
                    for _ in range(-dc):
                        self.piece.shift_left()
                self.piece.rotate()
                return
