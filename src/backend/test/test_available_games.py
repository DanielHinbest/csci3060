import pytest
from file_manager import AvailableGamesFileManager
from game import Game
from util import change_to_file_dir

# Global variable for use in both tests
games = [Game('Yoshi', 'ssuser03', 399.48), Game('Luigi', 'ssuser05', 921.42)]
file_name = 'test_available_games.txt'
change_to_file_dir(__file__)

def test_write():
    # Arrange
    available_games = AvailableGamesFileManager()

    # Act
    available_games.write(file_name, games)

    # Assert
    # Open the file and check that it contains the expected data
    with open(file_name, 'r') as file:
        lines = file.readlines()
        assert len(lines) == 3  # Expecting 2 games and an 'END' line
       # assert lines[0].strip() == 'Yoshi' + '_' * (24 - len('Yoshi')) + 'ssuser03________399.48'
        expected_yoshi_line = 'Yoshi' + '_' * (22) + 'ssuser03' + '_' * (8) + '399.48'
        assert lines[0].strip() == expected_yoshi_line
        assert lines[1].strip() == 'Luigi' + '_' * (22) + 'ssuser05________921.42'
        assert lines[2].strip() == 'END______________________________________________'

def test_read():
    # Arrange
    available_games = AvailableGamesFileManager()

    # Act
    read_games = available_games.read(file_name)

    # Assert
    assert len(read_games) == 2
    assert read_games[0].get_name() == 'Yoshi'
    assert read_games[0].get_seller() == 'ssuser03'
    assert read_games[0].get_price() == 399.48
    assert read_games[1].get_name() == 'Luigi'
    assert read_games[1].get_seller() == 'ssuser05'
    assert read_games[1].get_price() == 921.42