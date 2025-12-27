"""
This module provides a utility function to retrieve the local IP address of the machine.
"""
import socket


def get_local_ip():
    """
    Returns the local IP address used for network communication.
    
    Attempts to connect to a public DNS server to determine the correct interface.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connect to a public IP (Google DNS), doesn't send anything
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()
