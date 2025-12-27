"""
Tests for the GameState base class.
"""
from unittest.mock import MagicMock
from src.GameEngine.GameStates.game_state import GameState


class ConcreteGameState(GameState):
    """Concrete implementation of GameState for testing."""
    def update(self, dt, batch):
        """Mock update logic."""
        return self

    def get_renderer(self, batch):
        """Mock renderer retrieval."""
        return MagicMock()


def test_game_state_defaults():
    """Test default values and pass-through methods of the base class."""
    state = ConcreteGameState()
    assert state.next_state == state
    assert not state.is_ability_wrappable()

    # Check that pass methods don't raise errors
    state.on_move_down()
    state.on_move_up()
    state.on_move_left()
    state.on_move_right()
    state.on_hold_piece()
    state.on_select_option()
    state.on_reset(MagicMock())
    state.on_use_ability(0)


def test_game_state_is_ability_wrappable():
    """Test that the default wrappable check returns False."""
    state = ConcreteGameState()
    assert state.is_ability_wrappable() is False
