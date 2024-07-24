import pytest
import sys
import traceback
from transaction import Transaction
from user import User
from game import Game
from collection import Collection
from util import change_to_file_dir

class TestHandleDelete:
    @pytest.fixture
    def transaction(self):
        users_map = {"testuser": User("testuser", "AA", 0)}
        games_map = {"testgame": Game("testgame", "testuser", 1), "orphanedgame": Game("orphanedgame", "nonexistentuser", 10)}
        game_collection_map = {"testuser": Collection("test_game", "test_user")}
        # Change to Current File's Directory
        change_to_file_dir(__file__)
        log_file = "test_delete_log.txt"
        # Create log file and open for writing.
        log = open(log_file, "w+")
        return Transaction(users_map, games_map, game_collection_map, log)

    def test_handle_delete_user_exists(self, transaction):
        line = "02_testuser__________AA_000529.89"
        transaction.handle_transaction("02", line)
        assert "testuser" not in transaction.users_map
        # Ensure we're at the start of the file if it's going to be read again elsewhere
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "INFO: User testuser has been deleted.\n" in content

    def test_handle_delete_user_does_not_exist(self, transaction):
        line = "02_testuser2__________AA_000529.89"
        transaction.handle_transaction("02", line)
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "ERROR: User testuser2 does not exist.\n" in content

    def test_handle_delete_user_has_game_collection(self, transaction):
        line = "02_testuser__________AA_000529.89"
        transaction.handle_transaction("02", line)
        assert "testuser" not in transaction.game_collection_map
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "INFO: User testuser's games have been deleted.\n" in content

    def test_handle_delete_user_has_no_game_collection(self, transaction):
        del transaction.game_collection_map["testuser"]
        line = "02_testuser__________AA_000529.89"
        transaction.handle_transaction("02", line)
        assert "testuser" not in transaction.game_collection_map

    def test_handle_delete_user_has_games(self, transaction):
        line = "02_testuser__________AA_000529.89"
        transaction.handle_transaction("02", line)
        assert "testgame" not in transaction.games_map
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "INFO: Game testgame has been deleted.\n" in content

    def test_handle_delete_user_has_no_games(self, transaction):
        del transaction.games_map["testgame"]
        line = "02_testuser__________AA_000529.89"
        transaction.handle_transaction("02", line)
        assert "testgame" not in transaction.games_map
    
    def test_handle_delete_user_exists_games_in_one_map_only(self, transaction):
        # Edge case: User exists, but games are only in one map, not both
        del transaction.game_collection_map["testuser"]  # Pretend the games are only in games_map
        line = "02_testuser__________AA_000529.89"
        transaction.handle_transaction("02", line)
        assert "testuser" not in transaction.users_map
        assert "testgame" not in transaction.games_map
        self.check_log_content(transaction.log_file, [
            "INFO: User testuser has been deleted.",
            "INFO: Game testgame has been deleted."
        ])

    def test_handle_delete_nonexistent_user_with_no_games_or_collection(self, transaction):
        assert "nonexistentuser" not in transaction.users_map
        assert "nonexistentuser" not in transaction.game_collection_map
        line = "02_nonexistentuser____BB_000000.00"
        transaction.handle_delete(line)
        self.check_log_content(transaction.log_file, ["ERROR: User nonexistentuser does not exist.\n"])

    # Test that an orphaned game is deleted if the user does not exist in the users list.
    def test_handle_delete_nonexistent_user_with_games_no_collection(self, transaction):
        assert "nonexistentuser" not in transaction.users_map
        line = "02_nonexistentuser____BB_000000.00"
        transaction.handle_transaction("02", line)
        assert "orphanedgame" not in transaction.games_map
        print(transaction.games_map)
        self.check_log_content(transaction.log_file, ["ERROR: User nonexistentuser does not exist.\n", "INFO: Game orphanedgame has been deleted."])

    def test_handle_delete_nonexistent_user_with_collection_no_games(self, transaction):
        assert "nonexistentuser" not in transaction.users_map
        transaction.game_collection_map["nonexistentuser"] = ["orphanedgame"]
        line = "02_nonexistentuser____BB_000000.00"
        transaction.handle_transaction("02", line)
        assert "nonexistentuser" not in transaction.game_collection_map
        self.check_log_content(transaction.log_file, ["ERROR: User nonexistentuser does not exist.\n"])

    def test_handle_delete_nonexistent_user_with_games_and_collection(self, transaction):
        assert "nonexistentuser" not in transaction.users_map
        transaction.games_map["orphanedgame"] = Game("orphanedgame", "nonexistentuser", 10)
        transaction.game_collection_map["nonexistentuser"] = ["orphanedgame"]
        line = "02_nonexistentuser____BB_000000.00"
        transaction.handle_delete(line)
        assert "orphanedgame" not in transaction.games_map
        assert "nonexistentuser" not in transaction.game_collection_map
        self.check_log_content(transaction.log_file, ["ERROR: User nonexistentuser does not exist.\n", "INFO: Game orphanedgame has been deleted."])      

    @staticmethod
    def check_log_content(log_file, expected_messages):
        # Utility function to check log content
        log_file.seek(0)
        content = log_file.read()
        print(f"Content:{content}")
        for message in expected_messages:
            print(f"Message: {message}")
            assert message in content


class TestHandleCreate:
    @pytest.fixture
    def transaction(self):
        users_map = {"testuser": User("testuser", "AA", 0)}
        games_map = {"testgame": Game("testgame", "testuser", 1)}
        game_collection_map = {"testuser": ["testgame"]}
        log_file = "test.txt"
        # Create log file and open for writing.
        log = open(log_file, "r+")
        return Transaction(users_map, games_map, game_collection_map, log)

    def test_handle_create_user_already_exists(self, transaction):
        line = "01_testuser__________AA_000529.89"
        transaction.handle_transaction("01", line)
        assert "testuser" in transaction.users_map
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "ERROR: User testuser already exists.\n" in content

    def test_handle_create_user_does_not_exist(self, transaction):
        line = "01_testuser2__________AA_000529.89"
        transaction.handle_transaction("01", line)
        assert "testuser2" in transaction.users_map
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "INFO: User testuser2 has been created.\n" in content

class TestHandleSell:
    @pytest.fixture
    def transaction(self):
        users_map = {"testuser": User("testuser", "AA", 0)}
        games_map = {"testgame": Game("testgame", "testuser", 1)}
        game_collection_map = {"testuser": ["testgame"]}
        log_file = "test.txt"
        # Create log file and open for writing.
        log = open(log_file, "r+")
        return Transaction(users_map, games_map, game_collection_map, log)

    def test_handle_sell_game_already_exists(self, transaction):
        line = "SELL_testgame_testuser_1"
        transaction.handle_sell(line)
        assert "testgame" in transaction.games_map
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "ERROR: Game testgame already exists.\n" in content

    def test_handle_sell_new_game(self, transaction):
        line = "SELL_newgame_testuser_2"
        transaction.handle_sell(line)
        assert "newgame" in transaction.games_map
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "Game newgame has been added.\n" in content

    def test_handle_sell_invalid_price(self, transaction):
        line = "SELL_newgame_testuser_invalid"
        with pytest.raises(ValueError):
            transaction.handle_sell(line)

    def test_handle_sell_empty_game_name(self, transaction):
        line = "SELL__testuser_2"
        transaction.handle_sell(line)
        assert "" not in transaction.games_map
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "ERROR: Game name cannot be empty.\n" in content

class TestHandleBuy:
    @pytest.fixture
    def transaction(self):
        users_map = {"testuser": User("testuser", "AA", 10), "testseller": User("testseller", "AA", 0)}
        games_map = {"testgame": Game("testgame", "testseller", 5)}
        game_collection_map = {"testuser": [], "testseller": ["testgame"]}
        log_file = "test.txt"
        # Create log file and open for writing.
        log = open(log_file, "r+")
        return Transaction(users_map, games_map, game_collection_map, log)

    def test_handle_buy_game_does_not_exist(self, transaction):
        line = "BUY_nonexistentgame_testuser_testseller_5"
        transaction.handle_buy(line)
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "ERROR: Game nonexistentgame does not exist.\n" in content

    def test_handle_buy_buyer_does_not_exist(self, transaction):
        line = "BUY_testgame_nonexistentuser_testseller_5"
        transaction.handle_buy(line)
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "ERROR: User nonexistentuser does not exist.\n" in content

    def test_handle_buy_seller_does_not_exist(self, transaction):
        line = "BUY_testgame_testuser_nonexistentseller_5"
        transaction.handle_buy(line)
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "ERROR: User nonexistentseller does not exist.\n" in content

    def test_handle_buy_not_enough_credit(self, transaction):
        line = "BUY_testgame_testuser_testseller_15"
        transaction.handle_buy(line)
        transaction.log_file.seek(0)
        content = transaction.log_file.read()
        assert "ERROR: User testseller does not have enough credit to buy game testgame.\n" in content

    # def test_handle_buy_successful(self, transaction):
    #     # Ensure the buyer and seller exist and the buyer has enough credit
    #     transaction.users_map['testuser'] = User('testuser', 'type', 10)
    #     transaction.users_map['testseller'] = User('testseller', 'type', 0)
    #     transaction.games_map['testgame'] = Game('testgame', 'testseller', 5)

    #     line = "BUY_testgame_testuser_testseller_5"
    #     transaction.handle_buy(line)
    #     assert "testgame" not in transaction.games_map
