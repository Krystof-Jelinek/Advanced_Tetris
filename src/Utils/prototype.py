"""
This module defines the Prototype interface for objects that can copy themselves.
"""
from abc import ABC, abstractmethod
from typing import Self


class Prototype(ABC):
    """
    Prototype: objects that create independent copies of themselves.
    """
    @abstractmethod
    def clone(self) -> Self:
        """Returns an independent copy of this object."""
