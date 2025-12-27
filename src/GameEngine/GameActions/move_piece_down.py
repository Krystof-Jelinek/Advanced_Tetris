"""
This module defines the MovePieceDown action for moving the current piece down by one row.
"""
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_board import GameBoard
from src.GameComponents.score_board import ScoreBoard
from src.GameEngine.GameActions.game_action import GameAction


class MovePieceDown(GameAction):
    """
    Action that moves the current piece down and updates the score for soft drop.
    """
    def __init__(self, piece: TetrisPiece, board: GameBoard, score_board: ScoreBoard):
        """Initializes the action with piece, board, and score board."""
        self.piece = piece
        self.board = board
        self.score_board = score_board

    def execute(self):
        """Moves the piece down if the move is valid."""
        new_positions = self.piece.get_shifted_positions(-1, 0)
        if self.board.is_valid_move(new_positions):
            self.piece.shift_down()
            self.score_board.add_soft_drop_score()
