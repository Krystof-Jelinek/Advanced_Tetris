"""
This module defines the ControllerInputHandler class for handling gamepad input (e.g. PS5 DualSense).
"""
from pyglet.input import Controller, ControllerManager
from pyglet.math import Vec2

from src.GameEngine.game_manager import GameManager
from src.IOHandlers.Commands.hold_piece_command import HoldPieceCommand
from src.IOHandlers.Commands.move_down_command import MoveDownCommand
from src.IOHandlers.Commands.move_left_command import MoveLeftCommand
from src.IOHandlers.Commands.move_right_command import MoveRightCommand
from src.IOHandlers.Commands.move_up_command import MoveUpCommand
from src.IOHandlers.Commands.reset_game_command import ResetGameCommand
from src.IOHandlers.Commands.select_option_command import SelectOptionCommand
from src.IOHandlers.Commands.use_ability_command import UseAbilityCommand
from src.IOHandlers.InputHandlers.input_handler import InputHandler

class ControllerInputHandler(InputHandler):
    """
    Maps gamepad buttons to commands; the press/repeat logic is inherited from InputHandler.

    Button names follow the SDL layout, on a DualSense: cross = "a", circle = "b",
    square = "x", triangle = "y", L1/R1 = "leftshoulder"/"rightshoulder", options = "start".
    """
    def __init__(self, game_manager: "GameManager", controller_manager: ControllerManager):
        """Initializes the button map and starts listening for (re)connected controllers."""
        super().__init__(game_manager)
        self.button_map = {
            "dpleft": MoveLeftCommand(),
            "dpright": MoveRightCommand(),
            "dpdown": MoveDownCommand(),
            "dpup": MoveUpCommand(),
            "stickleft": MoveLeftCommand(),
            "stickright": MoveRightCommand(),
            "stickdown": MoveDownCommand(),
            "stickup": MoveUpCommand(),
            "a": SelectOptionCommand(),
            "b": HoldPieceCommand(),
            "y": MoveUpCommand(),
            "start": ResetGameCommand(),
            "leftshoulder": UseAbilityCommand(0),
            "rightshoulder": UseAbilityCommand(1),
        }
        self.stick_press_threshold = 0.6  # how far the stick must be pushed to count as pressed
        self.stick_release_threshold = 0.4  # how far back it must return to count as released
        self.controller_manager = controller_manager
        self.controller_manager.push_handlers(on_connect=self.on_connect,
                                              on_disconnect=self.on_disconnect)
        for controller in self.controller_manager.get_controllers():
            self.on_connect(controller)

    def get_command(self, input_id):
        """Returns the command mapped to the given button name."""
        return self.button_map.get(input_id)

    def on_connect(self, controller: Controller):
        """Opens a newly connected controller and subscribes to its events."""
        controller.open()
        controller.push_handlers(self)

    def on_disconnect(self, controller: Controller):
        """Unsubscribes from a disconnected controller and releases all held inputs."""
        controller.remove_handlers(self)
        for input_id in list(self.input_state):
            self.on_release(input_id)

    def on_button_press(self, _controller: Controller, button: str):
        """Forwards a button press to the shared press logic."""
        self.on_press(button)

    def on_button_release(self, _controller: Controller, button: str):
        """Forwards a button release to the shared release logic."""
        self.on_release(button)

    def on_dpad_motion(self, _controller: Controller, vector: Vec2):
        """Translates the d-pad direction vector into virtual dpleft/dpright/dpup/dpdown inputs."""
        self._set_held("dpleft", vector.x < 0)
        self._set_held("dpright", vector.x > 0)
        self._set_held("dpup", vector.y > 0)
        self._set_held("dpdown", vector.y < 0)

    def _set_held(self, input_id: str, held: bool):
        """Presses or releases a virtual input based on its current state."""
        if held:
            self.on_press(input_id)
        else:
            self.on_release(input_id)

    def on_stick_motion(self, _controller: Controller, stick: str, vector: Vec2):
        """Translates the left stick position into virtual stickleft/stickright/stickup/stickdown inputs."""
        if stick != "leftstick":
            return
        x, y = vector.x, vector.y
        # only the dominant axis counts, so pushing sideways never rotates by accident
        if abs(x) >= abs(y):
            y = 0.0
        else:
            x = 0.0
        self._update_stick_direction("stickleft", -x)
        self._update_stick_direction("stickright", x)
        self._update_stick_direction("stickup", y)
        self._update_stick_direction("stickdown", -y)

    def _update_stick_direction(self, input_id: str, value: float):
        """Presses or releases a stick direction using two thresholds, so the input does not flicker."""
        if value > self.stick_press_threshold:
            self.on_press(input_id)
        elif value < self.stick_release_threshold:
            self.on_release(input_id)
