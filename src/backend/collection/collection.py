
class Collection:
    """
    The Collection class represents a collection of games owned by a specific owner.

    Attributes:
        game_name (str): The name of the game in the collection.
        owner (str): The owner of the collection.

    Methods:
        __init__(self, game_name="", owner=""): Initializes a new instance of the Collection class.
        get_games(self): Returns a list of games in the collection.
        get_owner(self): Returns the owner of the collection.
        set_game_name(self, game_name): Sets the name of the game in the collection.
        set_owner(self, owner): Sets the owner of the collection.
        to_string(self): Returns a string representation of the collection in the format "game_name_owner".
    """

    def __init__(self, game_name="", owner=""):
        """
        Initializes a new instance of the Collection class.

        Args:
            game_name (str, optional): The name of the game in the collection. Defaults to an empty string.
            owner (str, optional): The owner of the collection. Defaults to an empty string.
        """
        self.games = [game_name]
        self.owner = owner

    def get_games(self):
        """
        Returns the name of the game in the collection.

        Returns:
            str: The name of the game in the collection.
        """
        return self.games

    def get_owner(self):
        """
        Returns the owner of the collection.

        Returns:
            str: The owner of the collection.
        """
        return self.owner

    def add_game(self, game_name):
        """
        Sets the name of the game in the collection.

        Args:
            game_name (str): The name of the game in the collection.
        """
        self.games.append(game_name)

    def set_owner(self, owner):
        """
        Sets the owner of the collection.

        Args:
            owner (str): The owner of the collection.
        """
        self.owner = owner

    def to_string(self):
        """
        Returns a string representation of the collection in the format "game_name_owner".

        Returns:
            str: A string representation of the collection.
        """
        return f"{self.game_name}_{self.owner}"