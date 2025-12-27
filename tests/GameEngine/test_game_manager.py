"""
Tests for the GameManager class.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch

import pytest

from src.GameEngine.game_manager import GameManager
from src.GameEngine.GameEvents.events import GameEvent


@pytest.fixture
def game_manager():
    """Fixture providing a GameManager with mocked graphics batch."""
    # Mock Batch to avoid pyglet issues
    with patch('pyglet.graphics.Batch'):
        return GameManager()


def test_game_manager_initialization(game_manager):
    """Test correct initialization of game manager components."""
    assert game_manager.event_bus is not None
    assert game_manager.game_state is not None
    assert game_manager.stored_abilities == []


def test_game_manager_set_game_state(game_manager):
    """Test updating the current game state."""
    mock_state = MagicMock()
    game_manager.set_game_state(mock_state)
    assert game_manager.game_state == mock_state


def test_game_manager_handle_send_message(game_manager):
    """Test that messages are correctly passed to the messaging system."""
    mock_msg = MagicMock()
    mock_messaging = MagicMock()
    game_manager.messaging_system = mock_messaging

    game_manager.handle_send_message(mock_msg)
    mock_messaging.send_message.assert_called_once_with(mock_msg)


def test_game_manager_store_active_abilities(game_manager):
    """Test storing abilities for later use."""
    abilities = [MagicMock(), MagicMock()]
    game_manager.store_active_abilities({"abilities": abilities})
    assert game_manager.stored_abilities == abilities


def test_game_manager_provide_active_abilities(game_manager):
    """Test pushing stored abilities back to the event bus."""
    abilities = [MagicMock()]
    game_manager.stored_abilities = abilities

    # We need to mock event_bus push_event
    game_manager.event_bus.push_event = MagicMock()
    game_manager.provide_active_abilities(None)

    game_manager.event_bus.push_event.assert_called_once_with(
        GameEvent.POST_ABILITIES, {"abilities": abilities}
    )


def test_game_manager_handle_messages(game_manager):
    """Test polling and processing incoming network messages."""
    mock_messaging = MagicMock()
    msg1 = MagicMock()
    msg2 = MagicMock()
    mock_messaging.receive_message.side_effect = [msg1, msg2, None]
    game_manager.messaging_system = mock_messaging

    with patch.object(game_manager, '_handle_message') as mock_handle:
        game_manager._handle_messages()
        assert mock_handle.call_count == 2
        mock_handle.assert_any_call(msg1)
        mock_handle.assert_any_call(msg2)


def test_game_manager_commands_proxies(game_manager):
    """Test that game manager delegates commands to the current state."""
    mock_state = MagicMock()
    game_manager.game_state = mock_state

    game_manager.on_move_down()
    mock_state.on_move_down.assert_called_once()

    game_manager.on_move_up()
    mock_state.on_move_up.assert_called_once()

    game_manager.on_move_left()
    mock_state.on_move_left.assert_called_once()

    game_manager.on_move_right()
    mock_state.on_move_right.assert_called_once()

    game_manager.on_hold_piece()
    mock_state.on_hold_piece.assert_called_once()

    game_manager.on_select_option()
    mock_state.on_select_option.assert_called_once()

    game_manager.on_use_ability(0)
    mock_state.on_use_ability.assert_called_once_with(0)
