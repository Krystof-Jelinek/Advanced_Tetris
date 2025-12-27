
"""
This module defines the KeyboardInputHandler class for handling keyboard input.
"""
from pyglet.window import key

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


class KeyboardInputHandler(InputHandler):
    """
    Processes keyboard events, manages key repeat logic, and issues commands to the GameManager.
    """
    def __init__(self, game_manager: "GameManager"):
        """Initializes the keyboard handler with a command map and internal state."""
        self.game_manager = game_manager
        self.key_map = {
            key.LEFT: MoveLeftCommand(),
            key.RIGHT: MoveRightCommand(),
            key.DOWN: MoveDownCommand(),
            key.UP: MoveUpCommand(),
            key.ENTER: SelectOptionCommand(),
            key.C: HoldPieceCommand(),
            key.R: ResetGameCommand(),
            key.Q: UseAbilityCommand(0),
            key.E: UseAbilityCommand(1),
        }
        self.key_state = {}  # tracks keys that are currently pressed
        self.repeat_timer = {}   # time since first press
        self.initial_delay = 0.3  # seconds before repeating
        self.repeat_rate = 0.05

    def on_key_press(self, symbol, _modifiers):
        """Processes key press events and starts the repeat timer."""
        if symbol not in self.key_state:
            self.key_state[symbol] = True
            self.repeat_timer[symbol] = -self.initial_delay  # negativní start = počká 0.3 s
            command = self.key_map.get(symbol)
            if command:
                self.game_manager.handle_command(command)

    def on_key_release(self, symbol, _modifiers):
        """Processes key release events and stops the repeat timer."""
        if symbol in self.key_state:
            self.key_state.pop(symbol)
            self.repeat_timer.pop(symbol, None)

    def poll(self, dt):
        """Updates repeat timers and issues repeated commands while keys are held."""
        for symbol in list(self.key_state):
            self.repeat_timer[symbol] += dt
            if self.repeat_timer[symbol] >= 0:
                command = self.key_map.get(symbol)
                if command:
                    self.game_manager.handle_command(command)
                self.repeat_timer[symbol] -= self.repeat_rate

    # speciall methods for input if the gamestate requires and provides it
    def on_text(self, text):
        """Forwards text input to the current game state if supported."""
        state = self.game_manager.get_game_state()
        if hasattr(state, "on_text"):
            state.on_text(text)

    def on_text_motion(self, motion):
        """Forwards text motion input to the current game state if supported."""
        state = self.game_manager.get_game_state()
        if hasattr(state, "on_text_motion"):
            state.on_text_motion(motion)
