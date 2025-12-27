"""
Tests for the DummyList utility.
"""
from src.Utils.dummy_list import DummyList


def test_dummy_list():
    """Test that DummyList returns None for any index and ignores assignments."""
    dl = DummyList()

    # Accessing any index should return None
    assert dl[0] is None
    assert dl[999] is None
    assert dl[-1] is None

    # Setting item should do nothing (no error)
    dl[0] = "test"
    assert dl[0] is None
