"""
This module defines the MovePieceRight action for moving the current piece right by one column.
"""
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_board import GameBoard
from src.GameEngine.GameActions.game_action import GameAction


class MovePieceRight(GameAction):
    """
    Action that moves the current piece to the right.
    """
    def __init__(self, piece: TetrisPiece, board: GameBoard):
        """Initializes the action with piece and board."""
        self.piece = piece
        self.board = board

    def execute(self):
        """Moves the piece right if the move is valid."""
        new_positions = self.piece.get_shifted_positions(0, +1)
        if self.board.is_valid_move(new_positions):
            self.piece.shift_right()
