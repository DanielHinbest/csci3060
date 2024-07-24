from file_manager import FileManager
from collection import Collection
import re
from collections import defaultdict

# Define constants for the files.
NEW_GAME_COLLECTION_FILE_PATH = "./storage/gamescollection.txt"
OLD_GAME_COLLECTION_FILE_PATH = "./storage/gamescollection.txt"

class GameCollectionFileManager(FileManager):
    """A class that manages the game collection file.

    This class inherits from the FileManager class and provides methods to read and write game collections to a file.

    Attributes:
        NEW_GAME_COLLECTION_FILE_PATH (str): The file path for the new game collection file.
        OLD_GAME_COLLECTION_FILE_PATH (str): The file path for the old game collection file.
    """

    def read(self, file_name):
        """Reads game collections from a file.

        Args:
            file_name (str): The name of the file to read from.

        Returns:
            list: A list of Collection objects representing the game collections read from the file.
        """
        game_collections = defaultdict(list)
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('END'):
                    break
                # Split the line by multiple underscores. Might not work for the edge case where there's 25 characters.
                parts = re.split('__+', line)
                game_name = parts[0]
                owner = parts[1]

                game_collections[owner].append(game_name)

        return game_collections

    def write(self, file_name, collections):
        """Writes game collections to a file.

        Args:
            file_name (str): The name of the file to write to.
            collections (list): A list of Collection objects representing the game collections to write.

        Returns:
            None
        """
        with open(file_name, 'w') as file:
            for owner, games in collections.items():
                for game in games:
                    file.write(f"{game.ljust(26, '_')}_{owner.ljust(15, '_')}\n")


                
            file.write('END_______________________________________\n')
