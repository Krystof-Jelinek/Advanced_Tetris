"""
Tests for connection-related multiplayer states (IPInputState, WaitingForConnectionState).
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from src.GameEngine.GameStates.ip_input_state import IPInputState
from src.GameEngine.GameStates.waiting_for_connection_state import WaitingForConnectionState
from src.MessagingSystem.GameMessages.seed_message import SeedMessage


@pytest.fixture
def mock_messaging():
    """Fixture providing a mocked messaging system."""
    return MagicMock()


@pytest.fixture
def mock_event_bus():
    """Fixture providing a mocked event bus."""
    return MagicMock()


def test_ip_input_state_text_entry(mock_messaging, mock_event_bus):
    """Test entering and editing IP address text."""
    state = IPInputState(mock_messaging, mock_event_bus)
    state.on_text("127.0.0.1:5000")
    assert state.input_text == "127.0.0.1:5000"

    # Backspace
    # pylint: disable=import-outside-toplevel
    from pyglet.window import key
    state.on_text_motion(key.MOTION_BACKSPACE)
    assert state.input_text == "127.0.0.1:500"


def test_ip_input_state_select_option(mock_messaging, mock_event_bus):
    """Test parsing the entered address and starting connection."""
    state = IPInputState(mock_messaging, mock_event_bus)
    state.input_text = "192.168.1.1:1234"
    state.on_select_option()

    assert mock_messaging.ip == "192.168.1.1"
    assert mock_messaging.port == 1234
    mock_messaging.start.assert_called_once()


def test_ip_input_state_update_transitions(mock_messaging, mock_event_bus):
    """Test state transitions upon receiving a seed message."""
    state = IPInputState(mock_messaging, mock_event_bus)
    mock_messaging.is_running.return_value = True

    mock_messaging.receive_message.return_value = None
    assert state.update(0.1, MagicMock()) == state

    # Seed message received
    seed_msg = SeedMessage(42)
    mock_messaging.receive_message.return_value = seed_msg

    with patch('src.GameEngine.GameStates.ip_input_state.MultiplayerPlayingState') as mock_multi_play:
        new_state = state.update(0.1, MagicMock())
        assert new_state == mock_multi_play.return_value
        mock_multi_play.assert_called_once_with(mock_messaging, mock_event_bus, 42)


def test_waiting_for_connection_state_update(mock_messaging, mock_event_bus):
    """Test that host generates and sends a seed upon client connection."""
    state = WaitingForConnectionState(mock_messaging, mock_event_bus)
    mock_messaging.is_running.return_value = True

    with patch('src.GameEngine.GameStates.waiting_for_connection_state.MultiplayerPlayingState') as mock_multi_play:
        new_state = state.update(0.1, MagicMock())
        assert new_state == mock_multi_play.return_value
        mock_messaging.send_message.assert_called_once()
        # Message sent should be a SeedMessage
        sent_msg = mock_messaging.send_message.call_args[0][0]
        assert isinstance(sent_msg, SeedMessage)
