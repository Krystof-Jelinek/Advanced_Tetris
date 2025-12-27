"""
This module contains the ScoreBoard class which tracks and displays the player's score.
"""
from typing import Optional

from pyglet.graphics import Batch
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label

from src.GameComponents.game_component import GameComponent
from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameEvents.events import GameEvent
from src.Renderers.renderer import Renderer
from src.Renderers.GameComponentRenderers.score_board_renderer import ScoreBoardRenderer


class ScoreBoard(GameComponent):
    """
    Tracks and updates the game score based on lines cleared and other events.
    """
    def __init__(self, event_bus: EventBus):
        """Initializes the scoreboard and subscribes to scoring events."""
        self.score = 0
        self.event_bus = event_bus
        self.event_bus.subscribe(GameEvent.LINES_CLEARED, self.add_line_clear_score)
        self.event_bus.subscribe(GameEvent.PIECE_EXPLOSION, self.on_piece_explosion)

        self.title_label: Optional[Label] = None
        self.score_label: Optional[Label] = None
        self.background: Optional[BorderedRectangle] = None

    def add_line_clear_score(self, data: dict):
        """Calculates and adds score based on the number of lines cleared."""
        num_of_lines = data["num_of_rows"]
        line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += line_scores.get(num_of_lines, 0)

    def on_piece_explosion(self, _data):
        """Adds score for a piece explosion event."""
        self.score += 200

    def get_score(self) -> int:
        """Returns the current total score."""
        return self.score

    def set_score(self, score: int) -> None:
        """Sets the score to a specific value."""
        self.score = score

    def add_soft_drop_score(self):
        """Adds score for manual soft dropping a piece."""
        # Every manual drop gives 1 point
        self.score += 1

    def get_renderer(self, batch: Batch) -> Renderer:
        """Returns the renderer for the scoreboard."""
        return ScoreBoardRenderer(batch)
