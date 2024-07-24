
class Game:
    """
    Represents a game object with its name, seller, and price.

    Attributes:
        name (str): The name of the game.
        seller (str): The seller of the game.
        price (float): The price of the game.

    Methods:
        set_name(name): Sets the name of the game.
        set_seller(seller): Sets the seller of the game.
        set_price(price): Sets the price of the game.
        get_name(): Returns the name of the game.
        get_seller(): Returns the seller of the game.
        get_price(): Returns the price of the game.
        to_string(): Returns a string representation of the game object.
    """

    def __init__(self, name="", seller="", price=0.0):
        """
        Initializes a new instance of the Game class.

        Args:
            name (str, optional): The name of the game. Defaults to an empty string.
            seller (str, optional): The seller of the game. Defaults to an empty string.
            price (float, optional): The price of the game. Defaults to 0.0.
        """
        self.name = name
        self.seller = seller
        self.price = price

    def set_name(self, name):
        """
        Sets the name of the game.

        Args:
            name (str): The name of the game.
        """
        self.name = name

    def set_seller(self, seller):
        """
        Sets the seller of the game.

        Args:
            seller (str): The seller of the game.
        """
        self.seller = seller

    def set_price(self, price):
        """
        Sets the price of the game.

        Args:
            price (float): The price of the game.
        """
        self.price = price

    def get_name(self):
        """
        Returns the name of the game.

        Returns:
            str: The name of the game.
        """
        return self.name

    def get_seller(self):
        """
        Returns the seller of the game.

        Returns:
            str: The seller of the game.
        """
        return self.seller

    def get_price(self):
        """
        Returns the price of the game.

        Returns:
            float: The price of the game.
        """
        return self.price

    def to_string(self):
        """
        Returns a string representation of the game object.

        Returns:
            str: A string representation of the game object.
        """
        return f"{self.name}_{self.seller}_{self.price:.2f}"