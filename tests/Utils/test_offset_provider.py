"""
Tests for the OffsetProvider class.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
import pytest
from src.Utils.offset_provider import OffsetProvider
from src.Utils.offset import Offset


@pytest.fixture
def offset_provider():
    """Fixture providing an OffsetProvider initialized with a mock window."""
    provider = OffsetProvider()
    mock_window = MagicMock()
    mock_window.width = 1000
    mock_window.height = 800
    provider.inicialize(mock_window)
    return provider


def test_offset_provider_initialization(offset_provider):
    """Test that the provider correctly stores the window reference."""
    assert offset_provider.window is not None
    assert offset_provider.window.width == 1000


def test_get_board_offset(offset_provider):
    """Test calculating the board's screen position."""
    offset = offset_provider.get_board_offset()
    assert isinstance(offset, Offset)
    # Just check if it's reproducible or sensible
    assert offset.x_offset > 0
    assert offset.y_offset > 0


def test_get_game_over_offset(offset_provider):
    """Test calculating the game over message position."""
    offset = offset_provider.get_game_over_offset()
    assert offset.x_offset == 500
    assert offset.y_offset == 400


def test_get_menu_offset(offset_provider):
    """Test calculating menu position based on number of options."""
    offset = offset_provider.get_menu_offset(3)
    assert isinstance(offset, Offset)
    assert offset.x_offset > 0


def test_get_waiting_table_offset(offset_provider):
    """Test calculating position for the waiting status table."""
    offset = offset_provider.get_waiting_table_offset()
    assert offset.x_offset == (1000 - 600) // 2
    assert offset.y_offset == (800 - 100) // 2
