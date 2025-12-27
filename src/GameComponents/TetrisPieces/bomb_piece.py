"""
This module defines the BombPiece, a special piece that explodes when dropped.
"""
from typing import TYPE_CHECKING

from pyglet.graphics import Batch

from src.Config.config import config
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameEngine.GameEvents.events import GameEvent
from src.Renderers.GameComponentRenderers.tetris_piece_renderer import TetrisPieceRenderer
from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState


class BombPiece(TetrisPiece):
    """
    A Tetris piece that triggers an explosion event upon landing.
    """
    def __init__(self, center_row: int, center_col: int, color=config.piece_colors["Bomb"]):
        """Initializes the bomb piece with no relative blocks and a specific color."""
        relative_blocks = []
        kicks = []
        super().__init__(center_row, center_col, relative_blocks, color, kicks)

    def get_next_piece_hint_offset(self) -> Offset:
        """Returns the rendering offset for the next piece hint."""
        return Offset(0, -config.next_piece_hint_y/5)

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the bomb piece."""
        return TetrisPieceRenderer(batch)

    def on_drop(self, game_state: "PlayingState"):
        """Triggers a PIECE_EXPLOSION event when the bomb lands."""
        game_state.get_event_bus().push_event(
            GameEvent.PIECE_EXPLOSION, {"row": self.center_square.grid_row, "col": self.center_square.grid_col}
        )

    def is_lockable(self) -> bool:
        """Bomb pieces are not lockable in the traditional sense; they explode instead."""
        return False
