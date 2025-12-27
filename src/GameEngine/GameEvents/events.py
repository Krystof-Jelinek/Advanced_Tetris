"""
This module defines the GameEvent enumeration used by the EventBus for component communication.
"""
from enum import Enum


class GameEvent(Enum):
    """
    Enumeration of all possible events that can be communicated via the EventBus.
    """
    LINES_CLEARED = "lines_cleared"
    GAME_STATE_CHANGE = "game_state_change"
    SEND_GAME_MESSAGE = "send_game_message"
    SET_ABILITIES = "set_abilities"
    GET_ABILITIES = "get_abilities"
    POST_ABILITIES = "post_abilities"
    PIECE_EXPLOSION = "piece_explosion"
