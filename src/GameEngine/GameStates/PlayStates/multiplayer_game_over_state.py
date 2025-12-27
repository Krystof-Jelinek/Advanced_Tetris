"""
This module defines the MultiplayerGameOverState for displaying results after a multiplayer match.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.graphics import Batch
from pyglet.text import Label

from src.GameEngine.GameStates.game_state import GameState
from src.IOHandlers.OutputHandlers.audio_handler import audio_handler
from src.Renderers.GameStateRenderers.multiplayer_game_over_state_renderer import MultiplayerGameOverStateRenderer
from src.Renderers.renderer import Renderer
if TYPE_CHECKING:
    from src.GameComponents.game_board import GameBoard
    from src.GameEngine.game_manager import GameManager


class MultiplayerGameOverState(GameState):
    """
    State representing the game over screen in multiplayer mode, showing both scores.
    """
    def __init__(self, my_score: int, enemy_score: int):
        """Initializes the multiplayer game over state with local and remote scores."""
        super().__init__()
        self.my_score = my_score
        self.enemy_score = enemy_score

        self.result_label: Optional[Label] = None
        self.my_score_label: Optional[Label] = None
        self.enemy_score_label: Optional[Label] = None
        audio_handler.stop_music()
        audio_handler.play_sound("resources/game_over_sound.wav")

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the multiplayer game over state."""
        return MultiplayerGameOverStateRenderer(batch)

    def update(self, dt: float, batch: Batch) -> "GameState":
        """Updates the state logic (none currently)."""
        return self

    def clear_rendered_objects(self):
        """Clears visual components to release resources."""
        self.result_label = None
        self.my_score_label = None
        self.enemy_score_label = None

    def on_reset(self, game_manager: "GameManager"):
        """Resets the game through the game manager."""
        self.clear_rendered_objects()
        game_manager.reset_self()

    def on_enemy_ended(self):
        """Called when the enemy game ends (no effect in game over screen)."""

    def update_enemy_score(self, new_score: int) -> None:
        """Updates the enemy score (no effect in game over screen)."""

    def update_enemy_board(self, board: "GameBoard"):
        """Updates the enemy board (no effect in game over screen)."""
