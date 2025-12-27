"""
This module defines the abstract base class for all messaging systems used for multiplayer communication.
"""
from abc import ABC, abstractmethod

from src.MessagingSystem.GameMessages.game_message import GameMessage


class MessagingSystem(ABC):
    """
    Abstract base class for sending and receiving game messages between players.
    """
    @abstractmethod
    def send_message(self, message: GameMessage) -> None:
        """Sends a game message to the connected peer."""

    @abstractmethod
    def receive_message(self) -> GameMessage:
        """Receives and returns a game message from the connected peer, if available."""
