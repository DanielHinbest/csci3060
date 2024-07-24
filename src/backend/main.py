# Main controls the running of the backend. The creation of the merged daily transaction file, 
# the updating and validation of the scripts, and the writing of the log file are all handled here.

import file_manager as fm
from user import User
from game import Game
from collection import Collection
from transaction import Transaction
from collections import defaultdict
import sys

# Log file path
LOG_FILE_PATH = "./src/backend/storage/log.txt"

# Global maps to store data
users_map = {}
games_map = {}
game_collection_map = defaultdict(list)

def fileParser(mergedDailyTransactionFile, log, game_collection_map, users_map, games_map):
    """
    Parse the merged daily transaction file and write the new input files for the frontend.

    Parameters:
    mergedDailyTransactionFile (str): The path to the merged daily transaction file.
    log (file): The log file object.

    Returns:
    None
    """

    # Create new user accounts, available games, and game collection files.
    newUsersAccounts = fm.NEW_USER_ACCOUNTS_FILE_PATH
    newAvailableGames = fm.NEW_AVAILABLE_GAMES_FILE_PATH
    newGameCollection = fm.NEW_GAME_COLLECTION_FILE_PATH

    # Initialize file managers
    user_file_manager = fm.UserAccountsFileManager()
    game_collection_file_manager = fm.GameCollectionFileManager()
    available_games_file_manager = fm.AvailableGamesFileManager()

    log.write("Processing transactions...\n")

    # Create an instance of the Transaction class
    transaction = Transaction(users_map, games_map, game_collection_map, log)

    # Iterate through the merged daily transaction file
    with open(mergedDailyTransactionFile, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Transaction code will be the first two characters of the line
            transaction_code = line[:2]

            if transaction_code == "00":
                continue

            # Replace the if-elif-else statements with a call to handle_transaction
            users_map, games_map, game_collection_map, log = transaction.handle_transaction(transaction_code, line)

    log.write("Transactions have been processed.\n")


    log.write("Writing new user accounts, game collections, and available games to storage...\n")    
    # Write the new user accounts, available games, and game collection files
    user_file_manager.write(newUsersAccounts, list(users_map.values()))

    # Write the new available games file
    available_games_file_manager.write(newAvailableGames, list(games_map.values()))

    # Write the new game collection file
    game_collection_file_manager.write(newGameCollection, game_collection_map)

    log.write("New user accounts, game collections, and available games have been written to storage.\n")

def main():
    """
    The main function that controls the running of the backend.

    Parameters:
    None

    Returns:
    None
    """
    

    # Initialize file managers
    user_file_manager = fm.UserAccountsFileManager()
    game_collection_file_manager = fm.GameCollectionFileManager()
    available_games_file_manager = fm.AvailableGamesFileManager()
    daily_transaction_file_manager = fm.DailyTransactionFileManager()  # Adjust the path as necessary

    # Create log file and open for writing.
    log = open(LOG_FILE_PATH, "w")

    log.write("Loading user accounts, game collections, and available games into memory...\n")  # Log the loading of the data
    # Populate the users_map from the user accounts file
    user_accounts = user_file_manager.read(fm.OLD_USER_ACCOUNTS_FILE_PATH)  # Adjust the path as necessary
    for user in user_accounts:
        users_map[user.get_username()] = user

    # Populate the games_map from the available games file
    available_games = available_games_file_manager.read(fm.OLD_AVAILABLE_GAMES_FILE_PATH)  # Adjust the path as necessary
    for game in available_games:
        games_map[game.get_name()] = game

    # Populate the game_collection_map from the game collections file
    game_collection_map = game_collection_file_manager.read(fm.OLD_GAME_COLLECTION_FILE_PATH)  # Adjust the path as necessary

    log.write("User accounts, game collections, and available games have been loaded into memory.\n")  # Log the loading of the 
    
    log.write("Creating merged daily transaction file...\n")  # Log the start of processing transactions

    # Check if command line argument is provided
    if len(sys.argv) > 1:
        merged_dtf = sys.argv[1]
    else:
        # Merge daily transaction files from yesterday
        merged_dtf = daily_transaction_file_manager.write()
        log.write("Merged daily transaction file has been created.\n")  # Log the creation of the merged daily transaction file
    
    
    if merged_dtf != "":  # This will combine all relevant files into one
        print("Merged daily transaction file has been created.")
    else:
        print("Failed to create the merged daily transaction file.")

    # Now, it is time to parse the merged daily transaction file and write the new input files for the frontend.
    fileParser(merged_dtf, log, game_collection_map, users_map, games_map)

    # Close the log file
    log.close()
    
if __name__ == "__main__":
    main()