import pytest
import main
import os
import file_manager as fm
from unittest.mock import MagicMock, patch
from user import User
from game import Game
from collection import Collection
from util import change_to_file_dir

class TestFileParser:
    @pytest.fixture
    def setup(self):
        # Setup
        users_map = {"test_user": User("test_user", "AA", 100)}
        games_map = {"test_game": Game("test_game", "test_user", 50)}
        game_collection_map = {"test_user": ["test_game"]}
        # Change to Current File's Directory
        change_to_file_dir(__file__)
        log_file = "test_main_fileParser_log.txt"
        open(log_file, 'w').close()  # clear the log file
        return users_map, games_map, game_collection_map, log_file

    def test_fileParser(self, setup):
        users_map, games_map, game_collection_map, log_file = setup

        # Open the log file
        log_file_obj = open(log_file, 'w')

        # Mock the Transaction class and its handle_transaction method
        with patch('main.Transaction') as mock_transaction:
            instance = mock_transaction.return_value
            instance.handle_transaction.return_value = users_map, games_map, game_collection_map, log_file_obj

            # Mock the file_manager classes and their write methods
            with patch('main.fm.UserAccountsFileManager') as mock_user_file_manager, \
                patch('main.fm.GameCollectionFileManager') as mock_game_collection_file_manager, \
                patch('main.fm.AvailableGamesFileManager') as mock_available_games_file_manager:

                user_file_manager_instance = mock_user_file_manager.return_value
                game_collection_file_manager_instance = mock_game_collection_file_manager.return_value
                available_games_file_manager_instance = mock_available_games_file_manager.return_value

                # Call the function
                main.fileParser('mergedDailyTransactionFile.txt', log_file_obj, user_file_manager_instance, game_collection_file_manager_instance, available_games_file_manager_instance)
                
        # Close the log file
        log_file_obj.close()

        # # Check the log file
        # with open(log_file, 'r') as file:
        #     log = file.read()
        #     assert "Processing transactions...\n" in log
        #     assert "Transactions have been processed.\n" in log
        #     assert "Writing new user accounts, game collections, and available games to storage...\n" in log
        #     assert "New user accounts, game collections, and available games have been written to storage.\n" in log

        # # Check that the mock methods were called
        # mock_transaction.assert_called()
        # instance.handle_transaction.assert_called()
        # user_file_manager_instance.write.assert_called()
        # game_collection_file_manager_instance.write.assert_called()
        # available_games_file_manager_instance.write.assert_called()



class TestMainFunction:
    @pytest.fixture
    def setup(self):
        # Setup
        users_map = {"test_user": User("test_user", "AA", 100)}
        games_map = {"test_game": Game("test_game", "test_user", 50)}
        game_collection_map = {"test_user": Collection("test_game", "test_user")}

        # Change to the base directory, "../../../" is used to go up three directories
        os.chdir("../../..")

        log_file = main.LOG_FILE_PATH
        return users_map, games_map, game_collection_map, log_file

    def test_main(self, setup):
        users_map, games_map, game_collection_map, log_file = setup

        # Open the log file
        log_file_obj = open(log_file, 'w')

        # Mock the file_manager classes and their read/write methods
        with patch('main.fm.UserAccountsFileManager') as mock_user_file_manager, \
             patch('main.fm.GameCollectionFileManager') as mock_game_collection_file_manager, \
             patch('main.fm.AvailableGamesFileManager') as mock_available_games_file_manager, \
             patch('main.fm.DailyTransactionFileManager') as mock_daily_transaction_file_manager, \
             patch('main.fileParser') as mock_file_parser:

            user_file_manager_instance = mock_user_file_manager.return_value
            game_collection_file_manager_instance = mock_game_collection_file_manager.return_value
            available_games_file_manager_instance = mock_available_games_file_manager.return_value
            daily_transaction_file_manager_instance = mock_daily_transaction_file_manager.return_value

            user_file_manager_instance.read.return_value = users_map.values()
            game_collection_file_manager_instance.read.return_value = game_collection_map.values()
            available_games_file_manager_instance.read.return_value = games_map.values()
            daily_transaction_file_manager_instance.write.return_value = 'mergedDailyTransactionFile.txt'

            # Call the function
            main.main()

        # Close the log file
        log_file_obj.close()

        # Check the log file
        with open(log_file, 'r') as file:
            log = file.read()
            # assert "Loading user accounts, game collections, and available games into memory...\n" in log
            # assert "User accounts, game collections, and available games have been loaded into memory.\n" in log
            # assert "Creating merged daily transaction file...\n" in log
            # assert "Merged daily transaction file has been created.\n" in log

        # Check that the mock methods were called
        # user_file_manager_instance.read.assert_called()
        # game_collection_file_manager_instance.read.assert_called()
        # available_games_file_manager_instance.read.assert_called()
        # daily_transaction_file_manager_instance.write.assert_called()
        # mock_file_parser.assert_called()