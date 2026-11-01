"""
This module defines the AudioHandler class, a singleton for managing game sound effects and music.
"""
import pyglet

from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameEvents.events import GameEvent
from src.Utils.resource_path import resource_path


class AudioHandler:
    """
    Singleton class that handles playing background music and sound effects.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        """Ensures that only one instance of AudioHandler exists."""
        if cls._instance is None:
            cls._instance = super(AudioHandler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initializes the audio handler with music and sound effect players."""
        if self._initialized:
            return
        self._initialized = True
        self.event_bus = None
        # ✅ define all instance attributes here
        self.music_player = pyglet.media.Player()
        self.music_player.volume = 0.2
        self.sfx_players: list[pyglet.media.Player] = []

    def set_event_bus(self, bus: EventBus):
        """Subscribes the audio handler to relevant game events."""
        self.event_bus = bus
        self.event_bus.subscribe(GameEvent.PIECE_EXPLOSION, self.explosion_sound)
        self.event_bus.subscribe(GameEvent.LINES_CLEARED, self.line_clear_sound)
        self.event_bus.subscribe(GameEvent.TIME_REWIND, self.time_rewind_sound)

    def line_clear_sound(self, _data):
        """Plays the line clear sound effect."""
        self.play_sound("resources/line_clear_sound.wav")

    def explosion_sound(self, _data):
        """Plays the explosion sound effect."""
        self.play_sound("resources/explosion_sound.wav")
        self.play_sound("resources/wilhelm_scream.wav")

    def time_rewind_sound(self, _data):
        """Plays the time rewind sound."""
        self.play_sound("resources/rewind_time_sound.wav")

    def play_sound(self, path):
        """Loads and plays a sound effect from the specified path."""
        try:
            full_path = resource_path(path)
            source = pyglet.media.load(full_path, streaming=False)
            player = pyglet.media.Player()
            player.queue(source)
            player.play()
            player.volume = 0.35
            self.sfx_players.append(player)
            self.sfx_players = [p for p in self.sfx_players if p.playing]
        except (FileNotFoundError, OSError) as e:
            print(f"[AudioHandler] Failed to play sound '{path}': {e}")

    def play_music(self, path, loop=True):
        """Loads and plays background music from the specified path."""
        try:
            full_path = resource_path(path)
            music = pyglet.media.load(full_path)
            self.music_player.queue(music)
            self.music_player.loop = loop
            self.music_player.play()
        except (FileNotFoundError, OSError) as e:
            print(f"[AudioHandler] Failed to play sound '{path}': {e}")

    def stop_music(self):
        """Pauses the current background music."""
        self.music_player.pause()


audio_handler = AudioHandler()
