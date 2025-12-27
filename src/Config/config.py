"""
This module handles the loading and providing of game configuration from a JSON file.
"""
import json
from pathlib import Path
from typing import Tuple, Dict


class Config:
    """
    Configuration class that loads settings from a JSON file and provides them as properties.
    """
    def __init__(self, path: str = None):
        """
        Initializes the Config object by loading data from the specified or default path.
        """
        if path is None:
            path = Path(__file__).parent / "config.json"
        else:
            path = Path(path)

        with open(path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

        self._board_color = tuple(self._data.get("board_color", [50, 50, 50]))
        self._piece_colors = {
            k: tuple(v) for k, v in self._data.get("piece_colors", {}).items()
        }

    @property
    def square_size(self) -> int:
        """Returns the size of a single square on the game board."""
        return self._data.get("square_size", 20)

    @property
    def board_rows(self) -> int:
        """Returns the number of rows on the game board."""
        return self._data.get("game_board_rows", 20)

    @property
    def board_cols(self) -> int:
        """Returns the number of columns on the game board."""
        return self._data.get("game_board_cols", 10)

    @property
    def board_color(self) -> Tuple[int, int, int]:
        """Returns the background color of the game board."""
        return self._board_color

    @property
    def piece_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Returns a dictionary mapping piece types to their colors."""
        return self._piece_colors

    @property
    def score_board_size_x(self) -> int:
        """Returns the horizontal size of the score board."""
        return self._data.get("score_board_size_x", 160)

    @property
    def score_board_size_y(self) -> int:
        """Returns the vertical size of the score board."""
        return self._data.get("score_board_size_y", 80)

    @property
    def ability_icon_x(self) -> int:
        """Returns the horizontal position or size of ability icons."""
        return self._data.get("ability_icon_x", 160)

    @property
    def ability_icon_y(self) -> int:
        """Returns the vertical position or size of ability icons."""
        return self._data.get("ability_icon_y", 160)

    @property
    def ability_image_size(self) -> int:
        """Returns the pixel size for ability images."""
        return self._data.get("ability_image_size", 100)

    @property
    def next_piece_hint_x(self) -> int:
        """Returns the horizontal position or size of the next piece hint."""
        return self._data.get("next_piece_hint_x", 160)

    @property
    def next_piece_hint_y(self) -> int:
        """Returns the vertical position or size of the next piece hint."""
        return self._data.get("next_piece_hint_y", 160)

    @property
    def piece_holder_x(self) -> int:
        """Returns the horizontal position or size of the piece holder."""
        return self._data.get("next_piece_hint_x", 160)

    @property
    def piece_holder_y(self) -> int:
        """Returns the vertical position or size of the piece holder."""
        return self._data.get("next_piece_hint_y", 160)

    @property
    def menu_option_x(self) -> int:
        """Returns the horizontal size of a menu option."""
        return self._data.get("menu_option_x", 200)

    @property
    def menu_option_y(self) -> int:
        """Returns the vertical size of a menu option."""
        return self._data.get("menu_option_y", 100)

    @property
    def menu_option_spacing(self) -> int:
        """Returns the spacing between menu options."""
        return self._data.get("menu_option_spacing", 130)


# singleton instance
config = Config()
