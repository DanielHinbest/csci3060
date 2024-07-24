from file_manager import FileManager
from game import Game
import re

# Define constants for the files.
NEW_AVAILABLE_GAMES_FILE_PATH = "./storage/availablegames.txt"
OLD_AVAILABLE_GAMES_FILE_PATH = "./storage/availablegames.txt"

class AvailableGamesFileManager(FileManager):
    """
    This class represents a file manager for available games.
    It inherits from the FileManager class.

    Attributes:
    - NEW_AVAILABLE_GAMES_FILE_PATH: A string representing the file path for the new available games file.
    - OLD_AVAILABLE_GAMES_FILE_PATH: A string representing the file path for the old available games file.

    Methods:
    - read(file_name): Reads the available games from the specified file and returns a list of Game objects.
    - write(file_name, games): Writes the given list of Game objects to the specified file.
    """

    def read(self, file_name):
        """
        Reads the available games from the specified file and returns a list of Game objects.

        Parameters:
        - file_name: A string representing the file name to read from.

        Returns:
        - A list of Game objects representing the available games.
        """
        available_games = []
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('END'):
                    break
                parts = re.split('_+', line.strip())
                name = '_'.join(parts[:-2]).strip().rstrip('_')
                seller = parts[-2].strip()
                price = float(parts[-1])
                available_games.append(Game(name, seller, price))
        return available_games

    def write(self, file_name, games):
        """
        Writes the given list of Game objects to the specified file.

        Parameters:
        - file_name: A string representing the file name to write to.
        - games: A list of Game objects to write.

        Returns:
        - None
        """
        with open(file_name, 'w') as file:
            for game in games:
                name = game.get_name() + ('_' * (24 - len(game.get_name())))
                seller = game.get_seller()
                price = '{:06.2f}'.format(game.get_price())
                file.write(f"{name.ljust(26, '_')}_{seller.ljust(15, '_')}_{price}\n")
            file.write('END______________________________________________\n')
