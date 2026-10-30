"""
Tests for the ControllerInputHandler.
"""
# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from pyglet.math import Vec2
from src.IOHandlers.InputHandlers.controller_input_handler import ControllerInputHandler
from src.IOHandlers.Commands.hold_piece_command import HoldPieceCommand
from src.IOHandlers.Commands.move_left_command import MoveLeftCommand


@pytest.fixture
def controller_handler():
    """Fixture providing a ControllerInputHandler with mocked managers and no connected controllers."""
    game_manager = MagicMock()
    controller_manager = MagicMock()
    controller_manager.get_controllers.return_value = []
    return ControllerInputHandler(game_manager, controller_manager), game_manager


def test_already_connected_controller_is_opened():
    """Controllers connected before the game starts are opened and subscribed to."""
    controller = MagicMock()
    controller_manager = MagicMock()
    controller_manager.get_controllers.return_value = [controller]

    handler = ControllerInputHandler(MagicMock(), controller_manager)

    controller.open.assert_called_once()
    controller.push_handlers.assert_called_once_with(handler)


def test_button_press_triggers_command(controller_handler):
    """Pressing a mapped button issues the corresponding command."""
    handler, manager = controller_handler
    handler.on_button_press(MagicMock(), "b")
    assert isinstance(manager.handle_command.call_args[0][0], HoldPieceCommand)


def test_dpad_left_repeats_until_released(controller_handler):
    """Holding d-pad left repeats MoveLeft after the delay and stops once centred."""
    handler, manager = controller_handler
    handler.on_dpad_motion(MagicMock(), Vec2(-1, 0))
    assert isinstance(manager.handle_command.call_args[0][0], MoveLeftCommand)

    manager.handle_command.reset_mock()
    handler.poll(0.35)
    manager.handle_command.assert_called()

    handler.on_dpad_motion(MagicMock(), Vec2(0, 0))
    manager.handle_command.reset_mock()
    handler.poll(1.0)
    manager.handle_command.assert_not_called()


def test_disconnect_releases_held_inputs(controller_handler):
    """Unplugging a controller while a button is held does not leave it repeating forever."""
    handler, manager = controller_handler
    controller = MagicMock()
    handler.on_connect(controller)
    handler.on_button_press(controller, "b")

    handler.on_disconnect(controller)
    manager.handle_command.reset_mock()
    handler.poll(1.0)

    manager.handle_command.assert_not_called()
    controller.remove_handlers.assert_called_once_with(handler)
