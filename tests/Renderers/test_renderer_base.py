"""
Tests for the base Renderer class.
"""
from unittest.mock import MagicMock
from src.Renderers.renderer import Renderer


class ConcreteRenderer(Renderer):
    """Concrete implementation of Renderer for testing."""
    def render(self, component, offset=None):
        """Mock render logic."""


def test_renderer_initialization():
    """Test initial state of a renderer."""
    mock_batch = MagicMock()
    renderer = ConcreteRenderer(mock_batch)
    assert renderer.batch == mock_batch
