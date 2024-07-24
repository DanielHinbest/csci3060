import pytest
from game import Game

class TestGame:
    # Test for the get_name() method
    def test_get_name(self):
        game = Game("a", "a", 0)
        assert game.get_name() == "a"

    # Test for the get_seller() method
    def test_get_seller(self):
        game = Game("a", "a", 0)
        assert game.get_seller() == "a"
    
    # Test for the get_price() method
    def test_get_price(self):
        game = Game("a", "a", 0)
        assert game.get_price() == 0
    
    # Test for the set_name() method
    def test_set_name(self):
        game = Game("a", "a", 0)
        game.set_name("b")
        assert game.get_name() == "b"

    # Test for the set_seller() method
    def test_set_seller(self):
        game = Game("a", "a", 0)
        game.set_seller("b")
        assert game.get_seller() == "b"

    # Test for the set_price() method
    def test_set_price(self):
        game = Game("a", "a", 0)
        game.set_price(1)
        assert game.get_price() == 1

    # Test for the to_string() method
    def test_to_string(self):
        game = Game("a", "a", 0)
        assert game.to_string() == "a_a_0.00"