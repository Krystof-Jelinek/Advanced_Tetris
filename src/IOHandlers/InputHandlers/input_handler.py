"""
This module defines the abstract base class for all input handlers.
"""
from abc import ABC, abstractmethod


class InputHandler(ABC):
    """
    Abstract base class for processing user input and translating it into game commands.
    """
    @abstractmethod
    def poll(self, dt):
        """Poll input device(s) and generate commands."""
