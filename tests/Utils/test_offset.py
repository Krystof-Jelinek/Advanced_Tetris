"""
Tests for the Offset utility class.
"""
from src.Utils.offset import Offset


def test_offset_initialization():
    """Test that Offset initializes with correct coordinates."""
    offset = Offset(10, 20)
    assert offset.x_offset == 10
    assert offset.y_offset == 20

    offset_default = Offset()
    assert offset_default.x_offset == 0
    assert offset_default.y_offset == 0


def test_apply_offset():
    """Test applying an offset to a pair of coordinates."""
    offset = Offset(5, -5)
    x, y = offset.apply_offset(10, 10)
    assert x == 15
    assert y == 5


def test_add_offset():
    """Test adding two Offset instances together."""
    offset1 = Offset(10, 20)
    offset2 = Offset(5, 5)

    result = offset1.add(offset2)
    assert result.x_offset == 15
    assert result.y_offset == 25

    # Original offsets should remain unchanged
    assert offset1.x_offset == 10
    assert offset1.y_offset == 20

    result_none = offset1.add(None)
    assert result_none.x_offset == 10
    assert result_none.y_offset == 20
