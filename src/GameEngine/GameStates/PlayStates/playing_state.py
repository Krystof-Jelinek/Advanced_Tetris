"""
This module contains the core PlayingState class which manages the Tetris gameplay logic.
"""
from pyglet.graphics import Batch

from src.Config.difficulty_settings import DifficultySettings
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece
from src.GameComponents.game_board import GameBoard
from src.GameComponents.next_piece_hint import NextPieceHint
from src.GameComponents.piece_holder import PieceHolder
from src.GameComponents.score_board import ScoreBoard
from src.GameComponents.shadow_piece_hint import ShadowPieceHint
from src.GameEngine.GameAbilities.ability import Ability
from src.GameEngine.GameAbilities.ability_system import AbilitySystem
from src.GameEngine.GameActions.game_action import GameAction
from src.GameEngine.GameActions.hold_piece import HoldPiece
from src.GameEngine.GameActions.move_piece_down import MovePieceDown
from src.GameEngine.GameActions.move_piece_left import MovePieceLeft
from src.GameEngine.GameActions.move_piece_right import MovePieceRight
from src.GameEngine.GameActions.rotate_piece import RotatePiece
from src.GameEngine.GameEvents.event_bus import EventBus
from src.GameEngine.GameEvents.events import GameEvent
from src.GameEngine.GameStates.PlayStates.game_over_state import GameOverState
from src.GameEngine.GameStates.game_state import GameState
from src.GameEngine.random_piece_generator import RandomPieceGenerator
from src.IOHandlers.OutputHandlers.audio_handler import audio_handler
from src.Renderers.GameStateRenderers.playing_state_renderer import PlayingStateRenderer
from src.Renderers.renderer import Renderer


# pylint: disable=too-many-public-methods
class PlayingState(GameState):
    """
    Main state for active gameplay, handling pieces, board, and scoring.
    """
    def __init__(self, event_bus: "EventBus", seed: int = None):
        """Initializes the playing state with game components and an optional seed."""
        super().__init__()
        self.board: GameBoard = GameBoard()
        self.piece_generator = RandomPieceGenerator(seed)
        self.event_bus = event_bus
        self.current_piece: TetrisPiece = self.piece_generator.get_next_piece()
        self.score_board = ScoreBoard(self.event_bus)
        self.next_piece_hint = NextPieceHint(self.piece_generator.peek_next_piece())
        self.piece_holder = PieceHolder()
        self.shadow_piece_hint = ShadowPieceHint(self.current_piece, self.board)
        self.ability_system = AbilitySystem(self, self.event_bus)

        self.event_bus.subscribe(GameEvent.POST_ABILITIES, self.set_active_abilities)
        self.event_bus.subscribe(GameEvent.PIECE_EXPLOSION, self.on_piece_explosion)

        self.next_state = self

        self.difficulty = DifficultySettings()

        self.time_modifier = 1  # this variable will be used in time affecting abilities

        audio_handler.play_music("resources/game_loop_sound.wav")
        #  this triggers a sequence of events that correctly setup the abilitySystems active abilities
        self.event_bus.push_event(GameEvent.GET_ABILITIES)

    def get_drop_interval(self) -> float:
        """Calculate current drop interval based on elapsed time."""
        t = min(self.difficulty.time_elapsed, self.difficulty.speedup_duration)
        time = self.difficulty.start_interval - (self.difficulty.start_interval - self.difficulty.min_interval) * (t / self.difficulty.speedup_duration)
        return time * self.time_modifier

    def update_time_modifier(self, time_modifier_update_value: float):
        """Updates the time modifier which affects the piece drop speed."""
        self.time_modifier = self.time_modifier * time_modifier_update_value

    def update(self, dt: float, batch: Batch) -> GameState:
        """Updates board state and handles piece gravity based on drop interval."""
        self.board.update(dt)

        self.difficulty.time_elapsed += dt
        self.difficulty.drop_timer += dt
        self.next_state = self
        # gradually decrease interval over time
        self.difficulty.drop_interval = self.get_drop_interval()

        if self.difficulty.drop_timer >= self.difficulty.drop_interval:
            self.difficulty.drop_timer = 0.0
            self.move_current_piece_down()  # this can set a new gamestate
        return self.next_state

    def move_current_piece_down(self):
        """Attempts to move the current piece down, locking it if impossible."""
        wanted_position = self.current_piece.get_shifted_positions(-1, 0)
        if self.board.is_valid_move(wanted_position):
            self.current_piece.shift_down()
        else:
            self.eval_piece_drop()  # piece locked

    def game_over(self):
        """Transitions the game to the game over state."""
        self.next_state = GameOverState(self.score_board.get_score())

    def eval_piece_drop(self):
        """Evaluates piece placement, line clears, and potential game over."""
        #  this means game over
        if not self.board.lock_piece_possible(self.current_piece):
            self.game_over()
            return
        self.current_piece.on_drop(self)
        self.board.lock_piece(self.current_piece)
        self.current_piece = self.piece_generator.get_next_piece()
        self.shadow_piece_hint.set_new_piece(self.current_piece)
        self.next_piece_hint.set_piece(self.piece_generator.peek_next_piece())
        self.piece_holder.reset_swap()

        squares_to_clear: list[tuple[int, int]] = []

        for row in range(self.board.rows - 1, -1, -1):
            is_row_full = all(not self.board[row][col].is_empty() for col in range(self.board.cols))

            if is_row_full:
                for col in range(self.board.cols):
                    if not self.board[row][col].is_empty() and self.board[row][col].is_clearable():
                        squares_to_clear.append((row, col))

        # Nyní 'squares_to_clear' obsahuje list[tuple[int, int]] všech políček z dokončených řádků
        if squares_to_clear:
            rows_to_check = set(r for r, c in squares_to_clear)
            scorable_rows_count = 0

            for row in rows_to_check:
                squares_in_row = [
                    self.board[r][c]
                    for r, c in squares_to_clear
                    if r == row
                ]
                is_row_scorable = all(square.is_scorable() for square in squares_in_row)

                if is_row_scorable:
                    scorable_rows_count += 1

            if scorable_rows_count > 0:
                self.event_bus.push_event(
                    GameEvent.LINES_CLEARED,
                    {"num_of_rows": scorable_rows_count}
                )
            # pylint: disable=import-outside-toplevel
            from src.GameEngine.GameStates.PlayStates.square_clearing_state import SquareClearingState
            self.next_state = SquareClearingState(self, squares_to_clear)

    def on_move_right(self):
        """Executes a move piece right action."""
        action: GameAction = MovePieceRight(self.current_piece, self.board)
        action.execute()

    def on_move_left(self):
        """Executes a move piece left action."""
        action: GameAction = MovePieceLeft(self.current_piece, self.board)
        action.execute()

    def on_move_up(self):
        """Executes a rotate piece action."""
        action: GameAction = RotatePiece(self.current_piece, self.board)
        action.execute()

    def on_move_down(self):
        """Executes a move piece down action, increasing score for soft drop."""
        action: GameAction = MovePieceDown(self.current_piece, self.board, self.score_board)
        action.execute()

    def on_hold_piece(self):
        """Executes a hold piece action."""
        action: GameAction = HoldPiece(self.piece_holder, self, self.shadow_piece_hint,
                                       self.next_piece_hint, self.piece_generator)
        action.execute()

    def on_use_ability(self, ability_index: int):
        """Triggers an ability by its index."""
        ability = self.ability_system.get_ability(ability_index)
        self.ability_system.resolve_ability(ability)

    def on_piece_explosion(self, _data):
        """Handles a piece explosion, marking surrounding clearable squares for removal."""
        center_row = self.current_piece.center_square.grid_row
        center_col = self.current_piece.center_square.grid_col

        squares_to_clear: list[tuple[int, int]] = []

        relative_coords_to_check = [
            (0, 0),

            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1),

            (-2, 0), (2, 0), (0, -2), (0, 2),
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2),

            (-2, -2), (-2, 2), (2, -2), (2, 2),

            (-3, 0), (3, 0), (0, -3), (0, 3),
        ]

        # 3. Kontrola políček
        for dr, dc in relative_coords_to_check:
            r = center_row + dr
            c = center_col + dc

            # Kontrola, zda je políčko uvnitř hrací desky
            if 0 <= r < self.board.rows and 0 <= c < self.board.cols:
                if self.board[r][c].is_clearable():
                    squares_to_clear.append((r, c))

        if squares_to_clear:
            # pylint: disable=import-outside-toplevel
            from src.GameEngine.GameStates.PlayStates.square_clearing_state import SquareClearingState
            self.next_state = SquareClearingState(self, squares_to_clear)

    def add_garbage_lines(self, num_lines: int = 3, duration: float = 20.0):
        """Adds garbage lines to the game board."""
        self.board.add_garbage_lines(num_lines, duration)

    def get_current_piece(self) -> TetrisPiece:
        """Returns the currently active Tetris piece."""
        return self.current_piece

    def get_ability_system(self):
        """Returns the ability system manager."""
        return self.ability_system

    def get_event_bus(self):
        """Returns the game event bus."""
        return self.event_bus

    def set_current_piece(self, new_piece: TetrisPiece):
        """Sets a new current piece and updates the shadow hint."""
        self.current_piece = new_piece
        self.shadow_piece_hint.set_new_piece(self.current_piece)

    def set_active_abilities(self, data: dict):
        """Sets the active abilities for the player."""
        abilities: list[Ability] = data["abilities"]
        self.ability_system.set_active_abilities(abilities)

    def generate_and_set_new_piece(self):
        """Generates a new piece and sets it as the current one."""
        self.current_piece = self.piece_generator.get_next_piece()

    def is_ability_wrappable(self) -> bool:
        """Indicates that this state can be wrapped for ability effects."""
        return True

    def get_renderer(self, batch: Batch) -> "Renderer":
        """Returns the renderer for the playing state."""
        return PlayingStateRenderer(batch)
