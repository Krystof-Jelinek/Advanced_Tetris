"""
This module defines the LanMessagingSystem class for TCP-based multiplayer communication.
"""
import json
import queue
import socket
import threading
import time
from typing import TYPE_CHECKING, Optional

import pyglet

from src.MessagingSystem.GameMessages.game_message import GameMessage
from src.MessagingSystem.messaging_system import MessagingSystem


if TYPE_CHECKING:
    pass


class LanMessagingSystem(MessagingSystem):
    """
    Handles network communication using TCP sockets for hosting and joining multiplayer games.
    """
    def __init__(self, is_host: bool, ip="0.0.0.0", port=5000):
        """Initializes the messaging system with network settings."""
        self.is_host = is_host
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.running = False

        self.receive_queue: queue.Queue[GameMessage] = queue.Queue()
        self.send_queue: queue.Queue[bytes] = queue.Queue()

    def is_running(self) -> bool:
        """Returns True if the messaging system is active and connected."""
        return self.running

    def start(self):
        """Starts the messaging system by either binding a port (host) or attempting a connection (client)."""
        self.sock.setblocking(False)
        if self.is_host:
            print("running bind")
            self.sock.bind((self.ip, self.port))
            self.sock.listen(1)

            # Schedule periodic attempts to accept
            pyglet.clock.schedule_interval(self.try_accept_connection, 1 / 30.0)

        else:
            print(f"Connecting to {self.ip}:{self.port} ...")
            pyglet.clock.schedule_interval(self.try_connect, 1 / 30.0)

    def try_accept_connection(self, _dt=None):
        """Attempts to accept an incoming client connection."""
        if self.conn:
            pyglet.clock.unschedule(self.try_accept_connection)
            return
        try:
            self.conn, addr = self.sock.accept()
            print(f"Client connected from {addr}")
            self.running = True
            threading.Thread(target=self._listen, daemon=True).start()
            threading.Thread(target=self._send, daemon=True).start()
        except BlockingIOError:
            # No connection yet;
            pass

    def try_connect(self, _dt=None):
        """Attempts to connect to a hosting player."""
        if self.conn:
            pyglet.clock.unschedule(self.try_connect)
            return  # already connected

        try:
            self.sock.setblocking(True)
            self.sock.connect((self.ip, self.port))
            self.sock.setblocking(False)
            self.conn = self.sock
            print("Connected to host")

            # Start listening & send threads
            self.running = True
            threading.Thread(target=self._listen, daemon=True).start()
            threading.Thread(target=self._send, daemon=True).start()

        except BlockingIOError:
            pass  # still trying, will be retried on next scheduled tick
        except (socket.error, ConnectionRefusedError, TimeoutError) as e:
            print("Connection error:", e)

    def _listen(self):
        """Background thread that listens for incoming data and parses messages."""
        buffer = ""
        while self.running:
            try:
                data = self.conn.recv(4096)
                if not data:
                    break
                buffer += data.decode()
                while "\n" in buffer:  # process all complete messages
                    line, buffer = buffer.split("\n", 1)
                    try:
                        msg = GameMessage.from_json(line)
                        self.receive_queue.put(msg)
                    except (json.JSONDecodeError, ValueError) as e:  # Konkrétní chyby v JSON/datech
                        print("Message decode error:", e)
            except BlockingIOError:
                time.sleep(0.01)
            except OSError as e:  # Konkrétní síťové chyby (socket.error, ConnectionReset, atd.)
                print("Receive error:", e)
                raise IOError("problem with lan messaging system -> in accepting messages") from e

    def _send(self):
        """Background thread that sends outgoing data from the send queue."""
        while True:
            if not self.conn:
                time.sleep(0.01)  # wait a bit if no connection
                continue
            try:
                data = self.send_queue.get(timeout=0.01)  # wait for a message
                self.conn.sendall(data)  # send blocking here, but thread won’t block main loop
            except queue.Empty:
                continue
            except Exception as e:
                print("Send error:", e)
                raise IOError("problem with lan messaging system -> in sending messages") from e

    def send_message(self, message: GameMessage):
        """Serializes and enqueues a message to be sent over the network."""
        if not self.conn:
            return
        try:
            data = (message.to_json() + "\n").encode()
            self.send_queue.put(data)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Send error:", e)

    def receive_message(self) -> Optional[GameMessage]:
        """Retrieves a message from the receive queue without blocking."""
        try:
            return self.receive_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        """Stops the messaging system and closes all network connections."""
        self.running = False
        if self.conn:
            self.conn.close()
        self.sock.close()
