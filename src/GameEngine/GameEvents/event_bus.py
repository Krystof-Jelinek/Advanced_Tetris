"""
This module contains the EventBus class, which facilitates decoupled communication between game components.
"""
from src.GameEngine.GameEvents.events import GameEvent


class EventBus:
    """
    A central hub for subscribing to and pushing game-wide events.
    
    This makes the system modular and reduces direct coupling between components.
    """
    def __init__(self):
        """Initializes the event bus with an empty listener dictionary."""
        self.listeners = {}

    def subscribe(self, event_name: GameEvent, callback):
        """Adds a callback function to the list of listeners for a specific event."""
        self.listeners.setdefault(event_name, []).append(callback)

    def unsubscribe(self, event_name: GameEvent, callback):
        """Removes a callback function from the list of listeners for a specific event."""
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)

    def push_event(self, event_name: GameEvent, data=None):
        """Triggers an event, calling all registered callbacks with the provided data."""
        for callback in self.listeners.get(event_name, []):
            callback(data)
