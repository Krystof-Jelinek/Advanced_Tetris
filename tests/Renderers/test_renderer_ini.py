"""
Tests for initializing all renderer subclasses.
"""
from unittest.mock import MagicMock
from src.Renderers.GameComponentRenderers.game_board_renderer import GameBoardRenderer
from src.Renderers.GameComponentRenderers.tetris_piece_renderer import TetrisPieceRenderer
from src.Renderers.GameComponentRenderers.score_board_renderer import ScoreBoardRenderer
from src.Renderers.GameComponentRenderers.next_piece_hint_renderer import NextPieceHintRenderer
from src.Renderers.GameComponentRenderers.piece_holder_renderer import PieceHolderRenderer
from src.Renderers.GameStateRenderers.menu_state_renderer import MenuStateRenderer
from src.Renderers.GameStateRenderers.playing_state_renderer import PlayingStateRenderer
from src.Renderers.TetrisSquareRenderers.board_square_renderer import BoardSquareRenderer
from src.Renderers.TetrisSquareRenderers.piece_square_renderer import PieceSquareRenderer


def test_renderers_initialization():
    """Test that all key renderers can be correctly instantiated with a graphics batch."""
    mock_batch = MagicMock()
    renderers = [
        GameBoardRenderer,
        TetrisPieceRenderer,
        ScoreBoardRenderer,
        NextPieceHintRenderer,
        PieceHolderRenderer,
        MenuStateRenderer,
        PlayingStateRenderer,
        BoardSquareRenderer,
        PieceSquareRenderer
    ]
    for renderer_cls in renderers:
        renderer = renderer_cls(mock_batch)
        assert renderer.batch == mock_batch
