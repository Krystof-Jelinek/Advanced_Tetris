"""
Tests that the rewind overlay is drawn where the board actually is on the screen.
"""
from unittest.mock import MagicMock, patch
import pytest
from src.Config.config import config
from src.Renderers.GameStateRenderers.rewind_state_renderer import RewindStateRenderer


@pytest.mark.parametrize("corner", [(490, 60), (290, 60)])  # single player board / multiplayer board moved left
def test_rewind_overlay_starts_at_the_board_corner(corner):
    """The tint and the label are placed on the board, wherever the game renderer drew it."""
    parent_state = MagicMock()
    parent_state.board[0][0].render_rect = MagicMock(x=corner[0], y=corner[1])
    rewind_state = MagicMock(overlay=None, label=None)
    rewind_state.get_parent_state.return_value = parent_state

    with patch("src.Renderers.GameStateRenderers.rewind_state_renderer.Rectangle") as rectangle, \
            patch("src.Renderers.GameStateRenderers.rewind_state_renderer.Label") as label:
        RewindStateRenderer(MagicMock()).render(rewind_state)

    assert rectangle.call_args.args[:2] == corner
    assert label.call_args.kwargs["x"] == corner[0] + config.board_cols * config.square_size / 2
    assert label.call_args.kwargs["y"] == corner[1] + config.board_rows * config.square_size / 2
