"""
This module contains the GameManager class which acts as the central controller for the game.
It manages game states, event bus, messaging system, and the main update/draw loops.
"""
from typing import Optional

from pyglet.graphics import Batch

from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameEvents.events import GameEvent
from src.GameEngine.GameStates.Menus.menu_state import MenuState
from src.GameEngine.GameStates.game_state import GameState
from src.IOHandlers.Commands.command import Command
from src.MessagingSystem.LANMessageSystem.lan_messaging_system import LanMessagingSystem
from src.MessagingSystem.GameMessages.game_message import GameMessage
from src.MessagingSystem.messaging_system import MessagingSystem


class GameManager:
    """
    Central manager for the game, coordinating states, events, and communication.
    """
    def __init__(self):
        """
        Initializes the GameManager, setting up the batch, event bus, and initial state.
        """
        self.batch = Batch()

        self.event_bus: EventBus = EventBus()
        self.event_bus.subscribe(GameEvent.GAME_STATE_CHANGE, self.set_game_state)
        self.event_bus.subscribe(GameEvent.SEND_GAME_MESSAGE, self.handle_send_message)
        self.event_bus.subscribe(GameEvent.SET_ABILITIES, self.store_active_abilities)
        self.event_bus.subscribe(GameEvent.GET_ABILITIES, self.provide_active_abilities)

        self.game_state = MenuState(self)  # starting with the menu statu which
        # is the only state that can acces and more importantly setup the gamemanager
        self.messaging_system: Optional[MessagingSystem] = None
        # this list servers as a storage for active abilities that will be then loaded into the playing state
        self.stored_abilities: list[Ability] = []

    def get_messaging_system(self) -> MessagingSystem:
        """Returns the current messaging system instance."""
        return self.messaging_system

    def get_event_bus(self) -> EventBus:
        """Returns the central event bus."""
        return self.event_bus

    def get_game_state(self) -> GameState:
        """Returns the current game state."""
        return self.game_state

    def set_game_state(self, game_state: GameState):
        """Updates the current game state."""
        self.game_state = game_state

    def update(self, dt: float):
        """
        Updates the current game state and handles incoming messages.
        """
        new_state: GameState = self.game_state.update(dt, self.batch)
        self.game_state = new_state
        self.game_state.get_renderer(self.batch).render(self.game_state)
        self._handle_messages()

    def store_active_abilities(self, abilities: dict):
        """Stores a list of active abilities for the playing state."""
        storable_abilities: list[Ability] = abilities["abilities"]
        self.stored_abilities = storable_abilities

    def provide_active_abilities(self, _data):
        """Pushes the stored abilities back onto the event bus."""
        self.event_bus.push_event(GameEvent.POST_ABILITIES, {"abilities": self.stored_abilities})

    def _handle_messages(self):
        """Polls and processes all pending messages from the messaging system."""
        if self.messaging_system is not None:
            while True:
                message = self.messaging_system.receive_message()
                if message is not None:
                    self._handle_message(message)
                else:
                    return

    def _handle_message(self, message: GameMessage):
        """Executes a single game message."""
        message.execute(self)

    def handle_send_message(self, message: GameMessage):
        """Sends a message through the messaging system if available."""
        if self.messaging_system is not None:
            self.messaging_system.send_message(message)

    def draw(self):
        """Renders the current batch."""
        self.batch.draw()

    def handle_command(self, command: Command):
        """Executes a game command."""
        command.execute(self)

    def on_move_down(self):
        """Delegates the move down action to the current state."""
        self.game_state.on_move_down()

    def on_move_up(self):
        """Delegates the move up action to the current state."""
        self.game_state.on_move_up()

    def on_move_left(self):
        """Delegates the move left action to the current state."""
        self.game_state.on_move_left()

    def on_move_right(self):
        """Delegates the move right action to the current state."""
        self.game_state.on_move_right()

    def on_hold_piece(self):
        """Delegates the hold piece action to the current state."""
        self.game_state.on_hold_piece()

    def on_select_option(self):
        """Delegates the select option action to the current state."""
        self.game_state.on_select_option()

    def on_reset(self):
        """Delegates the reset action to the current state."""
        self.game_state.on_reset(self)

    def on_use_ability(self, ability_index: int):
        """Delegates the use ability action to the current state."""
        self.game_state.on_use_ability(ability_index)

    def reset_self(self):
        """
        Resets the GameManager to its initial state, clearing the batch and event bus.
        """
        if self.messaging_system is not None and hasattr(self.messaging_system, "stop"):
            self.messaging_system.stop()
        self.batch = Batch()

        self.event_bus: EventBus = EventBus()
        self.event_bus.subscribe(GameEvent.GAME_STATE_CHANGE, self.set_game_state)
        self.event_bus.subscribe(GameEvent.SEND_GAME_MESSAGE, self.handle_send_message)
        self.event_bus.subscribe(GameEvent.SET_ABILITIES, self.store_active_abilities)
        self.event_bus.subscribe(GameEvent.GET_ABILITIES, self.provide_active_abilities)

        self.game_state = MenuState(self)  # starting with the menu statu which
        # is the only state that can acces and more importantly setup the gamemanager
        self.messaging_system: Optional[MessagingSystem] = None
        # this list servers as a storage for active abilities that will be then loaded into the playing state
        self.stored_abilities: list[Ability] = []

    def start_multiplayer(self, host: bool = True):
        """
        Initializes the multiplayer messaging system as either host or client.
        """
        if host:
            self.messaging_system = LanMessagingSystem(is_host=True)
            self.messaging_system.start()
        else:
            self.messaging_system = LanMessagingSystem(is_host=False)
            # system needs to be started later after the ip addres is inputed
