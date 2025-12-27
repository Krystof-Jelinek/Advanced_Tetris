"""
This module defines the BombPieceAbility class which transforms the current piece into a bomb.
"""
from typing import TYPE_CHECKING

import pyglet
from pyglet.image import AbstractImage

from src.Config.config import config
from src.GameComponents.TetrisPieces.bomb_piece import BombPiece
from src.Utils.resource_path import resource_path
from src.GameEngine.GameAbilities.ability import Ability

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class BombPieceAbility(Ability):
    """
    Ability that replaces the current piece with a special bomb piece.
    """
    def charge_ability(self, num_of_lines: int):
        """Charges the ability if lines are cleared."""
        if num_of_lines >= self.line_price:
            self.usable = True

    def __init__(self):
        """Initializes the bomb piece ability with its price."""
        super().__init__(line_price=3)

    def execute(self, game_state: "PlayingState"):
        """Replaces the current piece in the game state with a BombPiece."""
        game_state.set_current_piece(BombPiece(center_row=config.board_rows, center_col=int(config.board_cols/2)))

    def get_icon(self) -> AbstractImage:
        """Loads and returns the icon image for this ability."""
        return pyglet.image.load(resource_path("resources/ability_icons/bomb_piece_ability_icon.png"))
