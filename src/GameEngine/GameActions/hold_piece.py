"""
This module defines the HoldPiece action for swapping the current piece with the one in the holder.
"""
from typing import TYPE_CHECKING

from src.GameComponents.next_piece_hint import NextPieceHint
from src.GameComponents.shadow_piece_hint import ShadowPieceHint
from src.GameEngine.GameActions.game_action import GameAction
from src.GameEngine.random_piece_generator import RandomPieceGenerator

if TYPE_CHECKING:
    from src.GameComponents.piece_holder import PieceHolder
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class HoldPiece(GameAction):
    """
    Action that handles swapping the currently active piece with the piece in the holder.
    """
    def __init__(self,
                 piece_holder: "PieceHolder",
                 game_state: "PlayingState",
                 shadow_piece_hint: ShadowPieceHint,
                 next_piece_hint: NextPieceHint,
                 random_piece_generator: RandomPieceGenerator) -> None:
        """Initializes the hold piece action with all necessary game components."""
        self.piece_holder = piece_holder
        self.game_state = game_state
        self.shadow_piece_hint = shadow_piece_hint
        self.next_piece_hint = next_piece_hint
        self.random_piece_generator = random_piece_generator

    def execute(self):
        """Swaps the current piece with the holder and updates hints."""
        if self.piece_holder.is_empty():
            self.piece_holder.swap_piece(self.game_state.current_piece)
            self.game_state.generate_and_set_new_piece()
            self.shadow_piece_hint.set_new_piece(self.game_state.get_current_piece())
            self.next_piece_hint.set_piece(self.random_piece_generator.peek_next_piece())
        else:
            new_piece = self.piece_holder.swap_piece(self.game_state.get_current_piece())
            if new_piece is not None:
                self.game_state.set_current_piece(new_piece)
