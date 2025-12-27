"""
This module defines the SquareClearingStateRenderer.
"""
from typing import Optional, TYPE_CHECKING

from src.Renderers.renderer import Renderer
from src.Utils.offset import Offset

if TYPE_CHECKING:
    from src.GameEngine.GameStates.PlayStates.square_clearing_state import SquareClearingState


class SquareClearingStateRenderer(Renderer):
    """
    Renderer for the square clearing state, delegating to the parent playing state renderer.
    """
    def render(self, component: "SquareClearingState", offset: Optional[Offset] = None) -> None:
        """Forwards the rendering call to the parent state's renderer."""
        state = component.get_parent_state()
        state.get_renderer(self.batch).render(state, offset)
