"""
This module defines the abstract base class GameMessage and the registry for multiplayer messages.
"""
import json
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class GameMessage(ABC):
    """
    Abstract base class for all messages exchanged in multiplayer mode.
    """
    type: str = "base"

    def to_json(self) -> str:
        """Serializes the message to a JSON string."""
        return json.dumps({
            "type": self.type,
            "data": self.__dict__
        })

    @staticmethod
    def from_json(json_str: str) -> "GameMessage":
        """Deserializes a JSON string into an appropriate GameMessage instance."""
        obj = json.loads(json_str)
        msg_type = obj.get("type")
        data = obj.get("data", {})

        cls = MESSAGE_REGISTRY.get(msg_type)
        if not cls:
            raise ValueError(f"Unknown message type: {msg_type}")
        return cls(**data)

    @abstractmethod
    def execute(self, manager: "GameManager"):
        """Executes the message's logic on the given GameManager."""


MESSAGE_REGISTRY = {}


def register_message(cls):
    """Decorator to register a message class in the registry."""
    MESSAGE_REGISTRY[cls.type] = cls
    return cls
