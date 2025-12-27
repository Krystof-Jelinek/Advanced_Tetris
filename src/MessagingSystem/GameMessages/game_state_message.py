"""
This module defines the GameStateMessage, which synchronization the game state (score, board, piece) between players.
"""
from typing import TYPE_CHECKING

from src.Config.config import config
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.TetrisSquares.piece_square import PieceSquare
from src.GameComponents.game_board import GameBoard
from src.MessagingSystem.GameMessages.game_message import GameMessage, register_message

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


@register_message
class GameStateMessage(GameMessage):
    """
    Message containing the current state of a player's board, score, and active piece.
    """
    def execute(self, manager: "GameManager"):
        """Updates the local representation of the enemy's game state."""
        board = self.get_game_board()
        manager.get_game_state().update_enemy_board(board)
        manager.get_game_state().update_enemy_score(self.score)

    type: str = "game_state_message"

    @staticmethod
    def create_message(score: int, board: GameBoard, current_piece: TetrisPiece) -> "GameStateMessage":
        """Factory method to create a GameStateMessage from game objects."""
        # convert GameBoard -> list[list[tuple[int,int,int]]] for JSON
        new_board: list[list[tuple[int, int, int]]] = []
        for i in range(board.rows):
            row_colors: list[tuple[int, int, int]] = []
            for j in range(board.cols):
                square = board[i][j].color
                row_colors.append(square)
            new_board.append(row_colors)

        current_piece_coordinates: list[tuple[int, int]] = [
            (x, y)
            for (x, y) in current_piece.get_positions()
            if 0 <= x < board.rows and 0 <= y < board.cols
        ]
        current_piece_color = current_piece.color

        return GameStateMessage(score, new_board, current_piece_coordinates, current_piece_color)

    def __init__(self,
                 score: int,
                 board: list[list[tuple[int, int, int]]],
                 current_piece_coordinates: list[tuple[int, int]],
                 current_piece_color: tuple[int, int, int]):
        """Initializes the game state message with serialized data."""
        self.score: int = score
        self.board: list[list[tuple[int, int, int]]] = board
        self.current_piece_coordinates: list[tuple[int, int]] = current_piece_coordinates
        self.current_piece_color = current_piece_color

    def get_game_board(self) -> GameBoard:
        """Reconstructs a GameBoard object from the message data."""
        new_board = GameBoard()
        for i, row in enumerate(self.board):
            for j, color in enumerate(row):
                if tuple(color) != config.board_color:
                    new_board[i][j] = PieceSquare(i, j, 0, 0, color)
        for x, y in self.current_piece_coordinates:
            new_board[x][y] = PieceSquare(x, y, 0, 0, self.current_piece_color)
        return new_board

    def get_score(self) -> int:
        """Returns the score contained in the message."""
        return self.score
