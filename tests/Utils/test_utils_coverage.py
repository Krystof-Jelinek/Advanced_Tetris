"""
Tests for general utilities (resource_path, get_local_ip).
"""
import sys
import os
from unittest.mock import patch
from src.Utils.resource_path import resource_path
from src.Utils.get_local_ip import get_local_ip


def test_resource_path_no_meipass():
    """Test resource path calculation when not bundled."""
    # Ensure sys._MEIPASS is not there
    if hasattr(sys, "_MEIPASS"):
        del sys._MEIPASS

    path = "test/path"
    result = resource_path(path)
    assert os.path.abspath(".") in result
    assert path in result


def test_resource_path_with_meipass():
    """Test resource path calculation when bundled with PyInstaller."""
    with patch('sys._MEIPASS', '/tmp/meipass', create=True):
        path = "test/path"
        result = resource_path(path)
        assert result == os.path.join('/tmp/meipass', path)


def test_get_local_ip_success():
    """Test successfully retrieving the local IP address."""
    with patch('socket.socket') as mock_socket:
        mock_s = mock_socket.return_value
        mock_s.getsockname.return_value = ["192.168.1.10"]

        ip = get_local_ip()
        assert ip == "192.168.1.10"
        mock_s.connect.assert_called_once_with(("8.8.8.8", 80))


def test_get_local_ip_fail():
    """Test fallback to localhost when network is unavailable."""
    with patch('socket.socket') as mock_socket:
        _mock_s = mock_socket.return_value
        mock_socket.return_value.connect.side_effect = OSError("No route to host")

        ip = get_local_ip()
        assert ip == "127.0.0.1"
