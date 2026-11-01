"""
Tests for creating and restoring the mementos of the game components and of the whole PlayingState.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from src.GameComponents.TetrisPieces.bomb_piece import BombPiece
from src.GameComponents.TetrisPieces.line_piece import LinePiece
from src.GameComponents.TetrisPieces.t_piece import TPiece
from src.GameComponents.game_board import GameBoard
from src.GameComponents.piece_holder import PieceHolder
from src.GameComponents.score_board import ScoreBoard
from src.GameEngine.GameStates.PlayStates.playing_state import PlayingState
from src.GameEngine.random_piece_generator import RandomPieceGenerator


def describe_board(board):
    """Everything that matters about every square, independent of object identity."""
    return [(type(sq).__name__, sq.color, sq.grid_row, sq.grid_col, getattr(sq, "timer", None),
             getattr(sq, "is_locked", None)) for sq in board.iter_squares()]


def describe_holder(holder):
    """Held piece (class and positions) and the swap lock."""
    piece = holder.piece
    return (None if piece is None else (type(piece), piece.get_positions()), holder._swapped_this_turn)


def draw(generator, count):
    """Draws `count` pieces and returns their classes."""
    return [type(generator.get_next_piece()) for _ in range(count)]


@pytest.fixture
def playing_state():
    """Fixture providing a PlayingState with mocked audio."""
    with patch('src.IOHandlers.OutputHandlers.audio_handler.audio_handler.play_music'):
        return PlayingState(MagicMock(), seed=3)


def test_game_board_round_trip():
    """The board comes back exactly as saved, even after rows were cleared and garbage timers ran."""
    board = GameBoard()
    board.lock_piece(TPiece(1, 4))
    board.add_garbage_lines(2, duration=15.0)
    saved = describe_board(board)
    memento = board.create_memento()

    board.update(20.0)
    board.lock_piece(LinePiece(10, 4))
    board.clear_row(0)
    assert describe_board(board) != saved

    board.restore(memento)
    assert describe_board(board) == saved


def test_game_board_memento_can_be_restored_twice():
    """Restoring clones the saved squares, so the memento itself never changes."""
    board = GameBoard()
    board.lock_piece(TPiece(1, 4))
    saved = describe_board(board)
    memento = board.create_memento()

    board.restore(memento)
    board.clear_row(1)
    board.restore(memento)

    assert describe_board(board) == saved
    assert all(square is not saved_square
               for row, saved_row in zip(board.grid, memento.squares) for square, saved_square in zip(row, saved_row))


def test_piece_holder_round_trip():
    """A held, rotated piece and the swap lock come back."""
    holder = PieceHolder()
    piece = TPiece(10, 4)
    piece.rotate()
    holder.swap_piece(piece)
    saved = describe_holder(holder)
    memento = holder.create_memento()

    holder.reset_swap()
    holder.swap_piece(LinePiece(10, 4))
    holder.restore(memento)

    assert describe_holder(holder) == saved
    assert holder.piece is not memento.held_piece


def test_empty_piece_holder_round_trip():
    """An empty holder stays empty and unlocked after a restore."""
    holder = PieceHolder()
    memento = holder.create_memento()
    holder.swap_piece(TPiece(10, 4))
    holder.restore(memento)
    assert describe_holder(holder) == (None, False)


def test_score_board_round_trip():
    """The score comes back."""
    score_board = ScoreBoard(MagicMock())
    score_board.set_score(500)
    memento = score_board.create_memento()
    score_board.add_soft_drop_score()
    score_board.restore(memento)
    assert score_board.get_score() == 500


def test_generator_gives_the_same_pieces_again():
    """After a restore the same pieces come next, also after the bag was reshuffled."""
    generator = RandomPieceGenerator(seed=42)
    draw(generator, 3)
    memento = generator.create_memento()
    future = draw(generator, 16)

    generator.restore(memento)
    assert draw(generator, 16) == future


def test_playing_state_round_trip(playing_state):
    """The whole game (board, piece, holder, generator, score, difficulty) comes back."""
    playing_state.on_hold_piece()
    memento = playing_state.create_memento()
    saved = (describe_board(playing_state.board), type(playing_state.current_piece),
             playing_state.current_piece.get_positions(), describe_holder(playing_state.piece_holder),
             playing_state.score_board.get_score(), vars(playing_state.difficulty).copy())

    playing_state.board.add_garbage_lines(3)
    playing_state.set_current_piece(BombPiece(5, 5))
    playing_state.score_board.set_score(777)
    playing_state.difficulty.time_elapsed += 30
    playing_state.restore(memento)

    restored = (describe_board(playing_state.board), type(playing_state.current_piece),
                playing_state.current_piece.get_positions(), describe_holder(playing_state.piece_holder),
                playing_state.score_board.get_score(), vars(playing_state.difficulty).copy())
    assert restored == saved
    assert playing_state.shadow_piece_hint.piece is playing_state.current_piece


def test_playing_state_records_while_playing(playing_state):
    """Normal frames are recorded into the history."""
    for _ in range(30):
        playing_state.update(1 / 60, None)
    assert len(playing_state.get_history()) == 10


def test_playing_state_does_not_record_when_leaving(playing_state):
    """A frame that switches to another state (rows clearing, game over) is never recorded."""
    def leave():
        playing_state.next_state = MagicMock()

    playing_state.difficulty.drop_timer = 100  # the piece falls this frame
    with patch.object(playing_state, "move_current_piece_down", side_effect=leave):
        playing_state.update(0.1, None)
    assert len(playing_state.get_history()) == 0
