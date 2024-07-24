import re
from user import User
from game import Game
from config import MAX_CREDIT_LIMIT 
from collections import defaultdict

class Transaction:
    """
    The Transaction class represents a transaction in the system.
    It handles different types of transactions based on the transaction code.

    Attributes:
        CREATE_TRANSACTION (str): Constant representing the create transaction code.
        DELETE_TRANSACTION (str): Constant representing the delete transaction code.
        SELL_TRANSACTION (str): Constant representing the sell transaction code.
        BUY_TRANSACTION (str): Constant representing the buy transaction code.
        REFUND_TRANSACTION (str): Constant representing the refund transaction code.
        ADD_CREDIT_TRANSACTION (str): Constant representing the add credit transaction code.
        LIST_TRANSACTION (str): Constant representing the list transaction code.
        END_OF_SESSION_TRANSACTION (str): Constant representing the end of session transaction code.
        LOGIN_TRANSACTION (str): Constant representing the login transaction code.
        users_map (dict): A dictionary representing the users in the system.
        games_map (dict): A dictionary representing the games in the system.
        game_collection_map (dict): A dictionary representing the game collections in the system.
        log_file (str): The path to the log file.

    Methods:
        handle_create(): Handles the create transaction.
        handle_delete(): Handles the delete transaction.
        handle_sell(): Handles the sell transaction.
        handle_buy(): Handles the buy transaction.
        handle_refund(): Handles the refund transaction.
        handle_add_credit(): Handles the add credit transaction.
        handle_transaction(transaction_code): Handles the transaction based on the transaction code.

    """

    CREATE_TRANSACTION = "01"
    DELETE_TRANSACTION = "02"
    SELL_TRANSACTION = "03"
    BUY_TRANSACTION = "04"
    REFUND_TRANSACTION = "05"
    ADD_CREDIT_TRANSACTION = "06"
    LIST_TRANSACTION = "07"
    END_OF_SESSION_TRANSACTION = "00"

    def __init__(self, users_map, games_map, game_collection_map, log_file):
        """
        Initializes a new instance of the Transaction class.

        Args:
            users_map (dict): A dictionary representing the users in the system.
            games_map (dict): A dictionary representing the games in the system.
            game_collection_map (dict): A dictionary representing the game collections in the system.
            log_file (str): The path to the log file.
        """
        self.users_map = users_map
        self.games_map = games_map
        self.game_collection_map = game_collection_map
        self.log_file = log_file

    def handle_create(self, line):
        """
        Handles the create transaction.
        """

        # Extract the user information from the line
        parts = re.sub('_+', '_', line).strip().split('_')
        username = parts[1]
        user_type = parts[2]
        available_credit = float(parts[3])

        # Check if the username exists in the users map.
        if username in self.users_map:
            self.log_file.write(f"ERROR: User {username} already exists.\n")
        else:
            # Add the new user to the users map
            user = User(username, user_type, available_credit)
            self.users_map[username] = user
            self.log_file.write(f"INFO: User {username} has been created.\n")

    def handle_delete(self, line):
        """
        Handles the delete transaction.
        """

        # Extract the user information from the line
        parts = re.sub('_+', '_', line).strip().split('_')
        username = parts[1]

        # Check if the username exists in the users map.
        if username in self.users_map:
            # Remove the user from the users map
            del self.users_map[username]
            self.log_file.write(f"INFO: User {username} has been deleted.\n")
        else:
            self.log_file.write(f"ERROR: User {username} does not exist.\n")
        
        if username in self.game_collection_map:
            # Remove the user's games from the game collection map
            del self.game_collection_map[username]
            self.log_file.write(f"INFO: User {username}'s games have been deleted.\n")
            print(f"User {username}'s games have been deleted.")
        
        # Check if the user has any games in the games map.
        gamesToDelete = []
        for game in self.games_map:
            if self.games_map[game].get_seller() == username:
                # Remove the user's games from the games map
                gamesToDelete.append(game)
                self.log_file.write(f"INFO: User {username}'s games have been deleted.\n")

        # Remove the user's games from the games map
        for game in gamesToDelete:
            del self.games_map[game]
            self.log_file.write(f"INFO: Game {game} has been deleted.\n")


    def handle_sell(self, line):
        """
        Handles the sell transaction.
        """

        # Extract the game information from the line
        parts = re.sub('_+', '_', line).strip().split('_')
        game_name = '_'.join(parts[1:-2])
        seller = parts[-2]
        price = float(parts[-1])

        # Check if the game name is empty
        if not game_name:
            self.log_file.write("ERROR: Game name cannot be empty.\n")
            return

        # Check if the game exists in the games map.
        if game_name in self.games_map:
            self.log_file.write(f"ERROR: Game {game_name} already exists.\n")
        else:
            # Add the new game to the games map
            game = Game(game_name, seller, price)
            self.games_map[game_name] = game
            self.log_file.write(f"Game {game_name} has been added.\n")

    def handle_buy(self, line):
        """
        Handles the buy transaction.
        """

        # Extract the game information from the line
        parts = re.sub('_+', '_', line).strip().split('_')
        game_name = '_'.join(parts[1:-3])
        seller = parts[-3]
        buyer = parts[-2]
        price = float(parts[-1])

        # Check if the game exists in the games map.
        if game_name in self.games_map:
            # Check if the buyer exists in the users map.
            if buyer in self.users_map:
                # Check if the seller exists in the users map.
                if seller in self.users_map:
                    # Check if the buyer has enough credit to buy the game.
                    if self.users_map[buyer].get_credit() >= price:
                        # Update the buyer's available credit
                        self.users_map[buyer].set_available_credit(self.users_map[buyer].get_credit() - price)
                        # Update the seller's available credit
                        self.users_map[seller].set_available_credit(self.users_map[seller].get_credit() + price)
                        # Add the game to the buyer's game collection
                        self.game_collection_map[buyer].append(game_name)
                        self.log_file.write(f"Game {game_name} has been bought by {buyer}.\n")
                    else:
                        self.log_file.write(f"ERROR: User {buyer} does not have enough credit to buy game {game_name}.\n")
                else:
                    self.log_file.write(f"ERROR: User {seller} does not exist.\n")
            else:
                self.log_file.write(f"ERROR: User {buyer} does not exist.\n")
        else:
            self.log_file.write(f"ERROR: Game {game_name} does not exist.\n")

    # TODO: Should the game also be removed from the user's collection? Double Check
    # If so transaction format needs to be updated
    def handle_refund(self, line):
        """
        Handles the refund transaction.
        """
        # Extract information from the line
        # TODO: Change to split instead of substr?
        buyer_name = line[3:18].strip('_')
        seller_name = line[19:34].strip('_')
        refund_credit = float(line[35:43].strip('_'))
        
        # Check if the buyer exists in the users map
        if buyer_name in self.users_map:
            buyer_old_credit = self.users_map[buyer_name].get_credit()
            # Check if the seller exists in the users map
            if seller_name in self.users_map:
                seller_old_credit = self.users_map[seller_name].get_credit()
                # Check if the seller has enough credits
                if seller_old_credit >= refund_credit:
                    # Check if the seller can receive the credits (TODO: Double check if still add up to max or skip add)
                    if buyer_old_credit <= MAX_CREDIT_LIMIT:
                        self.users_map[seller_name].remove_credit(refund_credit)
                        self.log_file.write(f"INFO: {refund_credit} has been removed from seller {seller_name}. OLD: {seller_old_credit} NEW: {self.users_map[seller_name].get_credit()}\n")
                        self.users_map[buyer_name].add_credit(refund_credit)
                        self.log_file.write(f"INFO: Refund for buyer {buyer_name} has been processed. OLD: {buyer_old_credit} NEW: {self.users_map[buyer_name].get_credit()}\n")
                else:
                    self.log_file.write(f"ERROR: Seller {seller_name} does not have enough credits to process this refund.\n")
            else:
                self.log_file.write(f"ERROR: Seller {seller_name} does not exist.\n")
        else:
            self.log_file.write(f"ERROR: Buyer {buyer_name} does not exist.\n")

    def handle_add_credit(self, line):
        """
        Handles the add credit transaction.
        """
        #Extract user information from the line
        #Format: 06_UUUUUUUUUUUUUUU_TT_CCCCCCCCC
        parts = re.sub('_+', '_', line).strip().split('_')
        username = parts[1]
        #user_type = parts[2]
        available_credit = float(parts[3])

        self.log_file.write("Processing addcredit transaction\n")

        #Check if the user exists in the users map
        if username in self.users_map:
            #Update the user's available credit
            self.users_map[username].set_available_credit(float(available_credit))
            self.log_file.write(f"User {username}'s available credit has been updated to {available_credit}.\n")
        else:
            self.log_file.write(f"ERROR: User {username} does not exist.\n")

    def handle_transaction(self, transaction_code, line):
        """
        Handles the transaction based on the transaction code.

        Args:
            transaction_code (str): The transaction code.

        Returns:
            tuple: A tuple containing the updated users map, games map, game collection map, and log file.
        """
        if transaction_code == self.CREATE_TRANSACTION:
            self.handle_create(line)
        elif transaction_code == self.DELETE_TRANSACTION:
            self.handle_delete(line)
        elif transaction_code == self.SELL_TRANSACTION:
            self.handle_sell(line)
        elif transaction_code == self.BUY_TRANSACTION:
            self.handle_buy(line)
        elif transaction_code == self.REFUND_TRANSACTION:
            self.handle_refund(line)
        elif transaction_code == self.ADD_CREDIT_TRANSACTION:
            self.handle_add_credit(line)
        # else:
            #self.log_file.write("No further processing needed for transaction code: %s\n" % transaction_code)

        return self.users_map, self.games_map, self.game_collection_map, self.log_file
