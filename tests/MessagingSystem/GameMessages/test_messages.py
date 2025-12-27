"""
Tests for core game message serialization and reconstruction.
"""
import json
import pytest
from src.MessagingSystem.GameMessages.game_message import GameMessage
from src.MessagingSystem.GameMessages.seed_message import SeedMessage
from src.MessagingSystem.GameMessages.end_game_message import EndGameMessage
from src.MessagingSystem.GameMessages.game_state_message import GameStateMessage
from src.GameComponents.game_board import GameBoard
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


def test_seed_message_serialization():
    """Test serialization and deserialization of SeedMessage."""
    msg = SeedMessage(12345)
    json_str = msg.to_json()

    restored_msg = GameMessage.from_json(json_str)
    assert isinstance(restored_msg, SeedMessage)
    assert restored_msg.seed == 12345


def test_end_game_message_serialization():
    """Test serialization and deserialization of EndGameMessage."""
    msg = EndGameMessage()
    json_str = msg.to_json()

    restored_msg = GameMessage.from_json(json_str)
    assert isinstance(restored_msg, EndGameMessage)


def test_game_state_message_creation_and_serialization():
    """Test creating and serializing a GameStateMessage, including board reconstruction."""
    # Setup mock data
    board = GameBoard()
    # Create a piece
    piece = TetrisPiece(5, 5, [(0, 1)], (255, 0, 0))

    msg = GameStateMessage.create_message(100, board, piece)

    json_str = msg.to_json()
    restored_msg = GameMessage.from_json(json_str)

    assert isinstance(restored_msg, GameStateMessage)
    assert restored_msg.score == 100
    assert restored_msg.current_piece_color == list(piece.color)  # JSON converts tuple to list

    # Test get_game_board
    restored_board = restored_msg.get_game_board()
    assert isinstance(restored_board, GameBoard)


def test_invalid_message_type():
    """Test that unknown message types raise a ValueError."""
    invalid_json = json.dumps({"type": "unknown_type", "data": {}})
    with pytest.raises(ValueError, match="Unknown message type"):
        GameMessage.from_json(invalid_json)
