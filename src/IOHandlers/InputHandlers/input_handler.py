"""
This module defines the abstract base class for all input handlers.
"""

from abc import ABC, abstractmethod
from collections.abc import Hashable
from typing import TYPE_CHECKING, Optional, final

if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager
    from src.IOHandlers.Commands.command import Command

class InputHandler(ABC):
    """
    Abstract base class for processing user input and translating it into game commands.

    Template Method: the press -> repeat -> release algorithm is defined here,
    subclasses only provide the mapping from their raw inputs to commands.
    """
    def __init__(self, game_manager: "GameManager"):
        """Initializes the shared press/repeat state."""
        self.game_manager = game_manager
        self.input_state = {}  # inputs that are currently held
        self.repeat_timer = {}  # time since first press
        self.initial_delay = 0.3  # seconds before repeating
        self.repeat_rate = 0.05

    @abstractmethod
    def get_command(self, input_id: Hashable) -> Optional["Command"]:
        """Primitive step: returns the command mapped to the input, or None if unmapped."""

    @final
    def on_press(self, input_id: Hashable):
        """Issues the command once and starts the repeat timer."""
        if input_id in self.input_state:
            return
        self.input_state[input_id] = True
        self.repeat_timer[input_id] = -self.initial_delay  # negative start = waits initial_delay
        self._issue_command(input_id)

    @final
    def on_release(self, input_id: Hashable):
        """Stops the repeat timer of a released input."""
        if input_id in self.input_state:
            self.input_state.pop(input_id)
            self.repeat_timer.pop(input_id, None)

    @final
    def poll(self, dt: float):
        """Updates repeat timers and issues repeated commands while inputs are held."""
        for input_id in list(self.input_state):
            self.repeat_timer[input_id] += dt
            if self.repeat_timer[input_id] >= 0:
                self._issue_command(input_id)
                self.repeat_timer[input_id] -= self.repeat_rate

    def _issue_command(self, input_id: Hashable):
        """Looks up the command via the subclass step and sends it to the GameManager."""
        command = self.get_command(input_id)
        if command:
            self.game_manager.handle_command(command)
