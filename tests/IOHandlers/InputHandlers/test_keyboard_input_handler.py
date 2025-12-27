"""
Tests for the KeyboardInputHandler.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
import pytest
from pyglet.window import key
from src.IOHandlers.InputHandlers.keyboard_input_handler import KeyboardInputHandler
from src.IOHandlers.Commands.move_left_command import MoveLeftCommand


@pytest.fixture
def input_handler():
    """Fixture providing a KeyboardInputHandler with a mocked game manager."""
    mock_game_manager = MagicMock()
    handler = KeyboardInputHandler(mock_game_manager)
    return handler, mock_game_manager


def test_on_key_press_triggers_command(input_handler):
    """Test that pressing a key issues the corresponding command."""
    handler, manager = input_handler

    # Simulate LEFT key press
    handler.on_key_press(key.LEFT, 0)

    # Check if handle_command was called with MoveLeftCommand
    manager.handle_command.assert_called()
    called_command = manager.handle_command.call_args[0][0]
    assert isinstance(called_command, MoveLeftCommand)


def test_key_repeat_logic(input_handler):
    """Test key repeat mechanism after the initial delay."""
    handler, manager = input_handler

    # Press key
    handler.on_key_press(key.LEFT, 0)
    manager.handle_command.reset_mock()

    # Poll with small dt (less than initial delay 0.3)
    handler.poll(0.1)
    manager.handle_command.assert_not_called()

    # Poll until initial delay passed
    handler.poll(0.25)  # Total 0.35 > 0.3
    manager.handle_command.assert_called()
    manager.handle_command.reset_mock()

    # Poll with repeat rate (0.05)
    handler.poll(0.06)
    manager.handle_command.assert_called()


def test_on_key_release_stops_repeat(input_handler):
    """Test that releasing a key stops issuing repeat commands."""
    handler, manager = input_handler

    handler.on_key_press(key.LEFT, 0)
    handler.on_key_release(key.LEFT, 0)
    manager.handle_command.reset_mock()

    # Poll should not trigger more commands
    handler.poll(1.0)
    manager.handle_command.assert_not_called()
