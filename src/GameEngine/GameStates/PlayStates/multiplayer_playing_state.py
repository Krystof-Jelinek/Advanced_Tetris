"""
This module contains the MultiplayerPlayingState which extends the normal playing state with multiplayer features.
"""
from pyglet.graphics import Batch

from src.GameComponents.game_board import GameBoard
from src.GameComponents.score_board import ScoreBoard
from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameStates.game_state import GameState
from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
from src.MessagingSystem.GameMessages.end_game_message import EndGameMessage
from src.MessagingSystem.GameMessages.game_state_message import GameStateMessage
from src.MessagingSystem.messaging_system import MessagingSystem
from src.Renderers.GameStateRenderers.multiplayer_playing_state_renderer import MultiplayerPlayingStateRenderer
from src.Mementos.playing_state_memento import PlayingStateMemento
from src.Renderers.renderer import Renderer


class MultiplayerPlayingState(PlayingState):
    """
    Playing state with support for multiplayer synchronization and messaging.
    """
    def __init__(self, messaging_system: MessagingSystem, event_bus: "EventBus", seed: int = None):
        """Initializes the multiplayer playing state with networking and event bus."""
        super().__init__(event_bus, seed)
        self.messaging_system = messaging_system
        self.enemy_board = GameBoard()
        # this scoreboard shouldnt get acces to the "real" event bus since its updated from enemy scoring not my scoring
        self.enemy_score_board = ScoreBoard(EventBus())
        self.enemy_still_playing = True

    def update(self, dt: float, batch: Batch) -> GameState:
        """Updates game logic and sends the current state to the opponent."""
        state = super().update(dt, batch)
        self.send_state_to_enemy()
        return state

    def restore(self, memento: "PlayingStateMemento"):
        """Restores the game and shows the restored board to the opponent right away."""
        super().restore(memento)
        self.send_state_to_enemy()

    def send_state_to_enemy(self):
        """Sends the current board, piece and score to the opponent."""
        message = GameStateMessage.create_message(self.score_board.get_score(), self.board, self.current_piece)
        self.messaging_system.send_message(message)

    def game_over(self):
        """Signals game over to the opponent and transitions to waiting state."""
        message: EndGameMessage = EndGameMessage.create_message()
        self.messaging_system.send_message(message)
        # pylint: disable=import-outside-toplevel
        from src.GameEngine.GameStates.PlayStates.multiplayer_waiting_for_enemy_end_state import MultiplayerWaitingForEnemyEndState
        self.next_state = MultiplayerWaitingForEnemyEndState(self)

    def get_enemy_board(self) -> GameBoard:
        """Returns the board representing the opponent's game."""
        return self.enemy_board

    def get_enemy_score_board(self) -> ScoreBoard:
        """Returns the scoreboard of the opponent."""
        return self.enemy_score_board

    def update_enemy_score(self, new_score: int) -> None:
        """Updates the opponent's score with received data."""
        self.enemy_score_board.set_score(new_score)

    def update_enemy_board(self, board: GameBoard):
        """Updates the opponent's board visual state."""
        self.enemy_board.update_board_squares_colors(board)

    def is_enemy_playing(self) -> bool:
        """Returns True if the opponent is still playing."""
        return self.enemy_still_playing

    def on_enemy_ended(self):
        """Handler for when the opponent's game ends."""
        self.enemy_still_playing = False

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the multiplayer playing state."""
        return MultiplayerPlayingStateRenderer(batch)
