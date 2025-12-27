"""
This module contains the MultiplayerWaitingForEnemyEndState, used when one player finishes but the other is still playing.
"""
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.GameEngine.GameStates.game_state import GameState
from src.GameEngine.GameStates.PlayStates.multiplayer_game_over_state import MultiplayerGameOverState
from src.MessagingSystem.GameMessages.game_state_message import GameStateMessage
from src.GameEngine.GameStates.PlayStates.multiplayer_playing_state import MultiplayerPlayingState
if TYPE_CHECKING:
    pass


class MultiplayerWaitingForEnemyEndState(MultiplayerPlayingState):
    """
    Wrapper state that disables player input while waiting for the opponent to finish their game.
    """
    # pylint: disable=super-init-not-called
    def __init__(self, wrapped: "MultiplayerPlayingState"):
        """Initializes the state by wrapping an existing multiplayer playing state."""
        # intentionally not calling super().__init__()
        # because we are wrapping an existing instance
        self._wrapped = wrapped
        self.enemy_still_playing = self._wrapped.is_enemy_playing()

    def update(self, dt: float, batch: Batch) -> GameState:
        """Updates the game state, transitioning to game over once the opponent finished."""
        if not self.enemy_still_playing:
            return MultiplayerGameOverState(self.score_board.get_score(), self._wrapped.enemy_score_board.get_score())

        self._wrapped.update(dt, batch)
        message = GameStateMessage.create_message(self.score_board.get_score(), self.board, self.current_piece)
        self.messaging_system.send_message(message)
        return self

    def on_enemy_ended(self):
        """Handler for when the opponent's game ends."""
        self.enemy_still_playing = False

    def __getattr__(self, name):
        """Forwards attribute access to the wrapped playing state."""
        # forward everything to the wrapped state
        return getattr(self._wrapped, name)

    def on_move_right(self):
        """Disabled in waiting state."""

    def on_move_left(self):
        """Disabled in waiting state."""

    def on_move_up(self):
        """Disabled in waiting state."""

    def on_move_down(self):
        """Disabled in waiting state."""

    def on_hold_piece(self):
        """Disabled in waiting state."""
