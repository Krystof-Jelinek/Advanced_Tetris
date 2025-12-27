"""
Tests for all game command classes.
"""
# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
import pytest
from src.IOHandlers.Commands.move_down_command import MoveDownCommand
from src.IOHandlers.Commands.move_left_command import MoveLeftCommand
from src.IOHandlers.Commands.move_right_command import MoveRightCommand
from src.IOHandlers.Commands.move_up_command import MoveUpCommand
from src.IOHandlers.Commands.hold_piece_command import HoldPieceCommand
from src.IOHandlers.Commands.reset_game_command import ResetGameCommand
from src.IOHandlers.Commands.select_option_command import SelectOptionCommand
from src.IOHandlers.Commands.use_ability_command import UseAbilityCommand


@pytest.fixture
def mock_manager():
    """Fixture providing a mocked game manager."""
    return MagicMock()


def test_move_down_command(mock_manager):
    """Test executing the MoveDownCommand."""
    cmd = MoveDownCommand()
    cmd.execute(mock_manager)
    mock_manager.on_move_down.assert_called_once()


def test_move_left_command(mock_manager):
    """Test executing the MoveLeftCommand."""
    cmd = MoveLeftCommand()
    cmd.execute(mock_manager)
    mock_manager.on_move_left.assert_called_once()


def test_move_right_command(mock_manager):
    """Test executing the MoveRightCommand."""
    cmd = MoveRightCommand()
    cmd.execute(mock_manager)
    mock_manager.on_move_right.assert_called_once()


def test_move_up_command(mock_manager):
    """Test executing the MoveUpCommand."""
    cmd = MoveUpCommand()
    cmd.execute(mock_manager)
    mock_manager.on_move_up.assert_called_once()


def test_hold_piece_command(mock_manager):
    """Test executing the HoldPieceCommand."""
    cmd = HoldPieceCommand()
    cmd.execute(mock_manager)
    mock_manager.on_hold_piece.assert_called_once()


def test_reset_game_command(mock_manager):
    """Test executing the ResetGameCommand."""
    cmd = ResetGameCommand()
    cmd.execute(mock_manager)
    mock_manager.on_reset.assert_called_once()


def test_select_option_command(mock_manager):
    """Test executing the SelectOptionCommand."""
    cmd = SelectOptionCommand()
    cmd.execute(mock_manager)
    mock_manager.on_select_option.assert_called_once()


def test_use_ability_command(mock_manager):
    """Test executing the UseAbilityCommand with an index."""
    cmd = UseAbilityCommand(1)
    cmd.execute(mock_manager)
    mock_manager.on_use_ability.assert_called_once_with(ability_index=1)
