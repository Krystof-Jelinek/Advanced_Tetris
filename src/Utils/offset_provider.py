"""
This module defines the OffsetProvider class for calculating relative screen positions.
"""
from pyglet.window import Window

from src.Config.config import config
from src.Utils.offset import Offset


class OffsetProvider:
    """
    Utility class that calculates UI element positions based on the window size and game configuration.
    """
    def __init__(self):
        """Initializes the offset provider with no window attached."""
        self.window = None

    def inicialize(self, window: Window):
        """Attaches a pyglet window to the provider for coordinate calculations."""
        self.window = window

    def get_board_offset(self) -> Offset:
        """Calculates the offset to center the game board on the screen."""
        x = (self.window.width - config.board_cols * config.square_size) // 2
        y = (self.window.height - config.board_rows * config.square_size) // 2
        return Offset(x, y)

    def get_game_over_offset(self) -> Offset:
        """Calculates the offset for centering the game over message."""
        x = self.window.width // 2
        y = self.window.height // 2
        return Offset(x, y)

    def get_game_over_score_offset(self) -> Offset:
        """Calculates the offset for the score display on the game over screen."""
        sb_offset = self.get_scoreboard_offset()
        x = self.window.width // 2 - sb_offset.x_offset - config.score_board_size_x / 2
        y = self.window.height // 2 - sb_offset.y_offset - 2 * config.score_board_size_y
        return Offset(x, y)

    def get_scoreboard_offset(self) -> Offset:
        """Calculates the position for the player's scoreboard."""
        board_offset = self.get_board_offset()
        # Position one square left of the top of the board
        x = board_offset.x_offset - 6 * config.square_size
        y = board_offset.y_offset + config.board_rows
        return Offset(x, y)

    def get_next_piece_offset(self) -> Offset:
        """Calculates the position for the next piece hint."""
        board_offset = self.get_board_offset()
        x = board_offset.x_offset + config.board_cols * config.square_size + config.square_size
        y = board_offset.y_offset + config.board_rows * config.square_size
        return Offset(x, y)

    def get_piece_holder_offset(self):
        """Calculates the position for the piece holder."""
        board_offset = self.get_board_offset()
        # Position one square left of the top of the board
        x = board_offset.x_offset - 6.33 * config.square_size
        y = board_offset.y_offset + config.board_rows * config.square_size
        return Offset(x, y)

    def get_first_ability_offset(self) -> Offset:
        """Calculates the position for the first ability icon."""
        board_offset = self.get_board_offset()
        board_center_y = board_offset.y_offset + (config.board_rows * config.square_size) // 2

        # place to the left of the board
        x = board_offset.x_offset - config.square_size - config.ability_icon_x
        y = board_center_y - config.square_size
        return Offset(x, y)

    def get_second_ability_offset(self) -> Offset:
        """Calculates the position for the second ability icon."""
        board_offset = self.get_board_offset()
        board_center_y = board_offset.y_offset + (config.board_rows * config.square_size) // 2

        # place to the right of the board
        x = board_offset.x_offset + config.board_cols * config.square_size + config.square_size
        y = board_center_y - config.square_size
        return Offset(x, y)

    def get_menu_offset(self, num_options: int) -> Offset:
        """Calculates the base offset for a menu with a given number of options."""
        spacing = config.menu_option_spacing

        x = (self.window.width - config.menu_option_x) // 2

        total_height = num_options * config.menu_option_y + (num_options - 1) * spacing
        y = (self.window.height + total_height) // 2

        return Offset(x, y)

    def get_waiting_table_offset(self) -> Offset:
        """Calculates the offset for the waiting/connecting message table."""
        x = (self.window.width - 600) // 2
        y = (self.window.height - 100) // 2
        return Offset(x, y)


offsetProvider = OffsetProvider() # pylint: disable=invalid-name
