"""
Tests for the RandomPieceGenerator.
"""
from src.GameEngine.random_piece_generator import RandomPieceGenerator
from src.GameComponents.TetrisPieces.tetris_piece import TetrisPiece


def test_random_piece_generator_bag_logic():
    """Test that the generator uses a fair bag-shuffling mechanism."""
    generator = RandomPieceGenerator()
    # 7 pieces in a bag
    assert len(generator.bag) == 7

    # Draw all 7
    drawn = []
    for _ in range(7):
        drawn.append(generator.get_next_piece())

    assert len(generator.bag) == 0

    # Next draw should refill
    next_piece = generator.get_next_piece()
    assert len(generator.bag) == 6
    assert isinstance(next_piece, TetrisPiece)


def test_random_piece_generator_seed():
    """Test that identical seeds produce identical piece sequences."""
    seed = 42
    gen1 = RandomPieceGenerator(seed=seed)
    gen2 = RandomPieceGenerator(seed=seed)

    for _ in range(14):
        p1 = gen1.get_next_piece()
        p2 = gen2.get_next_piece()
        assert type(p1) is type(p2)


def test_peek_next_piece():
    """Test peeking at the next piece without removing it from the bag."""
    generator = RandomPieceGenerator()
    peeked_class = generator.peek_next_piece_class()
    peeked_instance = generator.peek_next_piece()
    drawn_instance = generator.get_next_piece()

    assert isinstance(drawn_instance, peeked_class)
    assert isinstance(peeked_instance, peeked_class)
