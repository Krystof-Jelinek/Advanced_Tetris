"""
This module defines the GameOverState for single player games.
"""
from typing import Optional, TYPE_CHECKING

from pyglet.graphics import Batch
from pyglet.text import Label

from src.GameComponents.score_board import ScoreBoard
from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameStates.game_state import GameState
from src.IOHandlers.OutputHandlers.audio_handler import audio_handler
from src.Renderers.GameStateRenderers.game_over_state_renderer import GameOverStateRenderer
from src.Renderers.renderer import Renderer
if TYPE_CHECKING:
    from src.GameEngine.game_manager import GameManager


class GameOverState(GameState):
    """
    State representing the game over screen in single player mode.
    """
    def __init__(self, score):
        """Initializes the game over state with the final score."""
        super().__init__()
        self.scoreboard = ScoreBoard(EventBus())
        self.scoreboard.set_score(score)
        self.game_over_label: Optional[Label] = None

        audio_handler.stop_music()
        audio_handler.play_sound("resources/game_over_sound.wav")

    def update(self, dt: float, batch: Batch) -> "GameState":
        """Updates the game over state logic (none currently)."""
        return self

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the game over state."""
        return GameOverStateRenderer(batch)

    def clear_rendered_objects(self):
        """Clears visual components to release resources."""
        self.game_over_label = None
        self.scoreboard = None

    def on_reset(self, game_manager: "GameManager"):
        """Resets the game through the game manager."""
        self.clear_rendered_objects()
        game_manager.reset_self()
