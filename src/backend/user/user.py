
class User:
    """
    Represents a user in the system.

    Attributes:
        username (str): The username of the user.
        user_type (str): The type of user (AA, FS, BS, or SS).
        available_credit (float): The amount of available credit for the user.
    """

    # Assuming USERNAME_FIELD_LENGTH is a predefined constant, add it here
    USERNAME_FIELD_LENGTH = 20  # Example value, adjust as needed (TODO: should be 15)

    def __init__(self, username="", user_type="", available_credit=0.0):
        """
        Initializes a new User object.

        Args:
            username (str, optional): The username of the user. Defaults to an empty string.
            user_type (str, optional): The type of user (AA, FS, BS, or SS). Defaults to an empty string.
            available_credit (float, optional): The amount of available credit for the user. Defaults to 0.0.
        """
        self.username = username
        self.user_type = user_type
        self.available_credit = available_credit

    def set_username(self, username):
        """
        Sets the username of the user.

        Args:
            username (str): The new username.

        Raises:
            ValueError: If the username exceeds the maximum length.
        """
        self.username = username

    def set_user_type(self, user_type):
        """
        Sets the type of user.

        Args:
            user_type (str): The new user type.

        Raises:
            ValueError: If the user type is not one of AA, FS, BS, or SS.
        """
        while user_type not in ["AA", "FS", "BS", "SS"]:
            print("The user type must be AA, FS, BS, or SS. Please try again.")
            user_type = input("Please enter a user type: ")
        self.user_type = user_type

    def add_credit(self, added_credits):
        """
        Adds credits to the user's available credit.

        Args:
            added_credits (float): The amount of credits to add.
        """
        self.available_credit += added_credits

    def remove_credit(self, removed_credits):
        """
        Removes credits from the user's available credit.

        Args:
            removed_credits (float): The amount of credits to remove.
        """
        self.available_credit -= removed_credits

    def set_available_credit(self, credit):
        # TODO: Validate credit input
        self.available_credit = credit

    def get_username(self):
        """
        Returns the username of the user.

        Returns:
            str: The username of the user.
        """
        return self.username

    def get_user_type(self):
        """
        Returns the type of user.

        Returns:
            str: The type of user.
        """
        return self.user_type

    def get_credit(self):
        """
        Returns the available credit of the user.

        Returns:
            float: The available credit of the user.
        """
        return self.available_credit
    
    def to_string(self):
        """
        Returns a string representation of the user.

        Returns:
            str: The string representation of the user in the format "username_user_type_available_credit".
        """
        return f"{self.username}_{self.user_type}_{self.available_credit:.2f}"
