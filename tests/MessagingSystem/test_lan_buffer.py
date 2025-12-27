"""
Tests for the network buffer processing logic.
"""
from unittest.mock import MagicMock
from src.MessagingSystem.LANMessageSystem.lan_messaging_system import LanMessagingSystem
from src.MessagingSystem.GameMessages.seed_message import SeedMessage


def test_lan_messaging_system_buffer_processing():
    """Test that the messaging system correctly serializes and deserializes messages from the JSON buffer."""
    system = LanMessagingSystem(is_host=False)
    system.conn = MagicMock()
    system.running = True

    # Message data
    msg = SeedMessage(123)
    data = (msg.to_json() + "\n").encode()

    # Mock conn.recv to return data then empty (or block)
    system.conn.recv.side_effect = [data, b'']
    # pylint: disable=import-outside-toplevel
    from src.MessagingSystem.GameMessages.game_message import GameMessage
    restored = GameMessage.from_json(msg.to_json())
    assert isinstance(restored, SeedMessage)
    assert restored.seed == 123
