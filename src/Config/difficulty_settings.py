"""
This module defines the difficulty settings for the game, controlling how the game speeds up over time.
"""
from dataclasses import dataclass


@dataclass
class DifficultySettings:
    """
    Data class representing the game's difficulty and timing parameters.
    """
    drop_timer: float = 0.0
    start_interval: float = 1.0
    drop_interval: float = 1.0
    time_elapsed: float = 0.0
    min_interval: float = 0.1
    speedup_duration: int = 10 * 60  # 10 minutes in seconds
