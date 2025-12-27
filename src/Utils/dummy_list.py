"""
This module defines the DummyList class, used to prevent out-of-bounds errors during rendering.
"""


class DummyList(list):
    """
    A list subclass that returns None for any index, preventing out-of-bounds crashes.
    
    It's used when a piece is partially off-board during generation.
    """
    def __getitem__(self, index):
        """Always returns None regardless of the index."""
        return None

    def __setitem__(self, index, value):
        """Does nothing when attempting to set an item."""
