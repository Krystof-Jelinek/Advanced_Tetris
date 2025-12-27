"""
This module defines the Offset class for handling 2D coordinate translations.
"""
from typing import Optional


class Offset:
    """
    Represents a displacement in 2D space (x, y).
    """
    def __init__(self, x_offset: int = 0, y_offset: int = 0):
        """Initializes the offset with x and y values."""
        self.x_offset = x_offset
        self.y_offset = y_offset

    def apply_offset(self, x: int, y: int) -> tuple[int, int]:
        """Applies the current offset to the given coordinates."""
        return x + self.x_offset, y + self.y_offset

    def add(self, other: Optional["Offset"]) -> "Offset":
        """Return a new Offset that is the sum of this and another Offset."""
        if other is None:
            return Offset(self.x_offset, self.y_offset)
        return Offset(self.x_offset + other.x_offset, self.y_offset + other.y_offset)
