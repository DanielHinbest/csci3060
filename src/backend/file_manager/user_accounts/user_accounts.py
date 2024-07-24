from file_manager import FileManager
from user import User

# Define a constant for the new user account file
NEW_USER_ACCOUNTS_FILE_PATH = "./storage/currentaccounts.txt"
OLD_USER_ACCOUNTS_FILE_PATH = "./storage/currentaccounts.txt"

class UserAccountsFileManager(FileManager):
    """
    This class represents a file manager for user accounts.
    It inherits from the FileManager class.

    Attributes:
    - NEW_USER_ACCOUNTS_FILE_PATH: A constant representing the file path for new user accounts.
    - OLD_USER_ACCOUNTS_FILE_PATH: A constant representing the file path for old user accounts.

    Methods:
    - read(file_name): Reads user accounts from a file and returns a list of User objects.
    - write(file_name, users): Writes user accounts to a file.

    Example Usage:
    file_manager = UserAccountsFileManager()
    users = file_manager.read('input_file.txt')  # Read users from a file
    file_manager.write('output_file.txt', users)  # Write users to a new file
    """
    def read(self, file_name):
        """
        Reads user accounts from a file and returns a list of User objects.

        Parameters:
        - file_name: A string representing the name of the file to read from.

        Returns:
        - user_accounts: A list of User objects representing the user accounts read from the file.
        """
        user_accounts = []
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == 'END_________________________':
                    break
                parts = [part for part in line.split('_') if part]  # Remove empty strings
                username = parts[0]
                user_type = parts[1]
                available_credit = float(parts[2].strip())  # Remove newline character
                user_accounts.append(User(username, user_type, available_credit))
        return user_accounts

    def write(self, file_name, users):
        """
        Writes user accounts to a file.

        Parameters:
        - file_name: A string representing the name of the file to write to.
        - users: A list of User objects representing the user accounts to write.

        Returns:
        - None
        """
        with open(file_name, 'w') as file:
            for user in users:
                username = user.username + ('_' * (16 - len(user.username)))
                user_type = user.user_type
                available_credit = '{:09.2f}'.format(user.available_credit)
                file.write(f"{username}{user_type}_{available_credit}\n")
            file.write('END_________________________\n')
