"""
Tests for the BombPiece.
"""
from unittest.mock import MagicMock
from src.GameComponents.TetrisPieces.bomb_piece import BombPiece
from src.GameEngine.GameEvents.events import GameEvent


def test_bomb_piece_initialization():
    """Test initial properties of the bomb piece."""
    piece = BombPiece(5, 5)
    assert piece.center_square.grid_row == 5
    assert piece.center_square.grid_col == 5
    assert len(piece.relative_squares) == 0  # Bomb is just one square
    assert not piece.is_lockable()


def test_bomb_piece_on_drop():
    """Test that the bomb piece triggers an explosion event on drop."""
    piece = BombPiece(5, 5)
    mock_game_state = MagicMock()
    mock_event_bus = MagicMock()
    mock_game_state.get_event_bus.return_value = mock_event_bus

    piece.on_drop(mock_game_state)

    mock_event_bus.push_event.assert_called_once_with(
        GameEvent.PIECE_EXPLOSION, {"row": 5, "col": 5}
    )
