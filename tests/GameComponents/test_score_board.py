"""
Tests for the ScoreBoard component.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
import pytest
from src.GameComponents.score_board import ScoreBoard
from src.GameEngine.GameEvents.events import GameEvent


@pytest.fixture
def score_board():
    """Fixture providing a ScoreBoard with a mocked event bus."""
    mock_event_bus = MagicMock()
    return ScoreBoard(mock_event_bus), mock_event_bus


def test_score_board_initialization(score_board):
    """Test initial score and event subscriptions."""
    sb, bus = score_board
    assert sb.get_score() == 0
    # Verify subscriptions
    calls = [call[0][0] for call in bus.subscribe.call_args_list]
    assert GameEvent.LINES_CLEARED in calls
    assert GameEvent.PIECE_EXPLOSION in calls


def test_add_line_clear_score(score_board):
    """Test score calculation for line clears."""
    sb, _ = score_board

    sb.add_line_clear_score({"num_of_rows": 1})
    assert sb.get_score() == 100

    sb.add_line_clear_score({"num_of_rows": 4})
    assert sb.get_score() == 100 + 800


def test_on_piece_explosion(score_board):
    """Test score bonus from piece explosion."""
    sb, _ = score_board
    sb.on_piece_explosion({})
    assert sb.get_score() == 200


def test_add_soft_drop_score(score_board):
    """Test score increment for soft drops."""
    sb, _ = score_board
    sb.add_soft_drop_score()
    assert sb.get_score() == 1
