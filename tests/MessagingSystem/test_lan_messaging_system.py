"""
Tests for the LanMessagingSystem networking class.
"""
from unittest.mock import MagicMock, patch
from src.MessagingSystem.LANMessageSystem.lan_messaging_system import LanMessagingSystem


def test_lan_messaging_system_initialization():
    """Test initial state of the LAN messaging system."""
    system = LanMessagingSystem(is_host=True)
    assert system.is_host
    assert not system.running
    assert system.receive_queue.empty()


@patch('socket.socket')
def test_lan_messaging_system_start_host(mock_socket_cls):
    """Test starting the system as a host (binding and listening)."""
    system = LanMessagingSystem(is_host=True, ip="127.0.0.1", port=1234)
    with patch('pyglet.clock.schedule_interval'):
        system.start()
        mock_socket_cls.return_value.bind.assert_called_with(("127.0.0.1", 1234))
        mock_socket_cls.return_value.listen.assert_called_with(1)


@patch('socket.socket')
def test_lan_messaging_system_send_message(_mock_socket_cls):
    """Test enqueuing a message for sending."""
    system = LanMessagingSystem(is_host=False)
    system.conn = MagicMock()

    mock_msg = MagicMock()
    mock_msg.to_json.return_value = '{"test": "data"}'

    system.send_message(mock_msg)
    assert system.send_queue.get() == b'{"test": "data"}\n'


def test_lan_messaging_system_receive_message():
    """Test receiving a message from the queue."""
    system = LanMessagingSystem(is_host=False)
    mock_msg = MagicMock()
    system.receive_queue.put(mock_msg)

    received = system.receive_message()
    assert received == mock_msg
    assert system.receive_message() is None


def test_lan_messaging_system_stop():
    """Test stopping the system and closing connections."""
    with patch('socket.socket'):
        system = LanMessagingSystem(is_host=True)
        mock_conn = MagicMock()
        system.conn = mock_conn
        system.running = True

        system.stop()
        assert not system.running
        # pylint: disable=no-member
        mock_conn.close.assert_called_once()
        # pylint: disable=no-member
        system.sock.close.assert_called_once()
