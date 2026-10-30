"""
Tests for the InputHandler template method.
"""
# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from src.IOHandlers.InputHandlers.input_handler import InputHandler


class FakeInputHandler(InputHandler):
    """Minimal subclass that only provides the primitive step, as every real handler does."""
    def __init__(self, game_manager, command_map):
        """Initializes the handler with a plain dict of input -> command."""
        super().__init__(game_manager)
        self.command_map = command_map

    def get_command(self, input_id):
        """Returns the command mapped to the given input."""
        return self.command_map.get(input_id)


@pytest.fixture
def fake_handler():
    """Fixture providing a FakeInputHandler with one mapped input and a mocked game manager."""
    game_manager = MagicMock()
    command = MagicMock()
    return FakeInputHandler(game_manager, {"fire": command}), game_manager, command


def test_press_issues_command_from_subclass_step(fake_handler):
    """The template asks the subclass for the command and sends it to the game manager."""
    handler, manager, command = fake_handler
    handler.on_press("fire")
    manager.handle_command.assert_called_once_with(command)


def test_unmapped_input_issues_nothing(fake_handler):
    """An input the subclass does not map is ignored, even when held."""
    handler, manager, _ = fake_handler
    handler.on_press("unknown")
    handler.poll(1.0)
    manager.handle_command.assert_not_called()


def test_holding_press_does_not_restart_delay(fake_handler):
    """A second press of an already held input neither issues a command nor resets the timer."""
    handler, manager, _ = fake_handler
    handler.on_press("fire")
    handler.poll(0.2)
    handler.on_press("fire")
    manager.handle_command.reset_mock()

    handler.poll(0.15)  # 0.35 s since the first press > 0.3 s initial delay
    manager.handle_command.assert_called_once()
