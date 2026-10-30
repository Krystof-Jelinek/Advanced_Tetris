
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
    Maps keyboard keys to commands; the press/repeat logic is inherited from InputHandler.
    """
    def __init__(self, game_manager: "GameManager"):
        """Initializes the keyboard handler with a command map."""
        super().__init__(game_manager)
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

    def get_command(self, input_id):
        """Returns the command mapped to the given key symbol."""
        return self.key_map.get(input_id)

    def on_key_press(self, symbol, _modifiers):
        """Forwards a key press to the shared press logic."""
        self.on_press(symbol)

    def on_key_release(self, symbol, _modifiers):
        """Forwards a key release to the shared release logic."""
        self.on_release(symbol)

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
