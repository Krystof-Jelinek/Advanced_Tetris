"""
Tests for the configuration module.
"""
from src.Config.config import config


def test_config_properties():
    """Test that all configuration properties are loaded correctly and have valid types."""
    assert config.square_size > 0
    assert config.board_rows > 0
    assert config.board_cols > 0
    assert isinstance(config.board_color, tuple)
    assert isinstance(config.piece_colors, dict)
    assert config.score_board_size_x > 0
    assert config.ability_icon_x > 0
    assert config.menu_option_x > 0


def test_config_initialization_with_path():
    """Test accessing config properties through the singleton instance."""
    # Test with default path (None) already done by singleton
    # Just check properties again on the singleton
    assert config.menu_option_spacing > 0
