"""
Tests for the NextPieceHint component.
"""
from unittest.mock import MagicMock
from src.GameComponents.next_piece_hint import NextPieceHint


def test_next_piece_hint_set_piece():
    """Test that the next piece hint updates its piece correctly."""
    mock_piece1 = MagicMock()
    mock_piece2 = MagicMock()

    hint = NextPieceHint(mock_piece1)
    assert hint.piece == mock_piece1

    hint.set_piece(mock_piece2)
    assert hint.piece == mock_piece2
