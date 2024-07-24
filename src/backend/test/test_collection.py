import pytest
from collection import Collection
from util import change_to_file_dir

class TestCollection:
    @pytest.fixture
    def collection(self):
        return Collection("test_game", "test_owner")

    # def test_init(self):
    #     collection = Collection("test_game", "test_owner")
    #     assert collection.get_games == ["test_game"]
    #     assert collection.owner == "test_owner"

    def test_get_game_name(self, collection):
        assert collection.get_games() == ["test_game"]

    def test_get_owner(self, collection):
        assert collection.get_owner() == "test_owner"

    # def test_set_game_name(self, collection):
    #     collection.add_game("new_game")
    #     assert collection.get_games == ["test_game", "new_game"]

    def test_set_owner(self, collection):
        collection.set_owner("new_owner")
        assert collection.owner == "new_owner"

    def test_to_string(self, collection):
        assert "test_game_test_owner" == "test_game_test_owner"