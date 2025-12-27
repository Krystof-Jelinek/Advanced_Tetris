"""
Tests for the AudioHandler class.
"""
from unittest.mock import MagicMock, patch
import pytest
from src.IOHandlers.OutputHandlers.audio_handler import audio_handler, AudioHandler
from src.GameEngine.GameEvents.events import GameEvent


@pytest.fixture(autouse=True)
def mock_pyglet_media():
    """Global fixture to mock pyglet media components during audio tests."""
    with patch.object(audio_handler.music_player, 'play'), \
         patch.object(audio_handler.music_player, 'queue'), \
         patch('pyglet.media.load'):
        yield


def test_audio_handler_singleton():
    """Test that AudioHandler follows the singleton pattern."""
    handler1 = AudioHandler()
    handler2 = AudioHandler()
    assert handler1 is handler2


def test_audio_handler_set_event_bus():
    """Test subscribing the audio handler to game events via the bus."""
    mock_bus = MagicMock()
    audio_handler.set_event_bus(mock_bus)

    # Check subscriptions
    calls = [call[0][0] for call in mock_bus.subscribe.call_args_list]
    assert GameEvent.PIECE_EXPLOSION in calls
    assert GameEvent.LINES_CLEARED in calls


def test_audio_handler_play_music():
    """Test starting background music."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.resource_path', return_value="test.wav"):
        with patch('pyglet.media.load') as mock_load:
            audio_handler.play_music("test.wav")
            mock_load.assert_called_once()
            audio_handler.music_player.play.assert_called_once()


def test_audio_handler_play_sound():
    """Test playing a sound effect."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.resource_path', return_value="test_sfx.wav"):
        with patch('pyglet.media.load') as mock_load:
            # We need to mock Player() call inside play_sound
            with patch('pyglet.media.Player') as mock_player_cls:
                audio_handler.play_sound("test_sfx.wav")
                mock_load.assert_called_once()
                mock_player_cls.return_value.play.assert_called_once()
