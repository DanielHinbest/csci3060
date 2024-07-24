#include <iostream>
#include <vector>
#include "TransactionHandler.h"
#include "FileReader.h"
#include "User.h"
#include "SharedData.h"
#include <string>
#include <chrono>

#define STORAGE_PATH "./storage/"
#define DAILY_TRANSACTION_FILE_LOCATION "./storage/daily_transactions/"

// Updated to use command-line arguments
int main(int argc, char *argv[])
{
    // Get the file names from the command line arguments
    std::string userAccountsFile;
    std::string availableGamesFile;
    std::string gameCollectionFile;
    std::string dailyTransactionFile;

    // Check if the correct number of arguments is passed
    if (argc < 4)
    {
        std::cerr << "Usage: " << argv[0] << " <users_filename>" << std::endl;
        return 1; // Return with error code
    } else if (argc == 5)
    {
        // When 5 arguments are provided we expect the system to be in testing mode.
        userAccountsFile = std::string(argv[1]);
        availableGamesFile =  std::string(argv[2]);
        gameCollectionFile =  std::string(argv[3]);
        dailyTransactionFile = std::string(argv[4]);
    } else 
    {
        // When 4 arguments are provided we expect the system to be in production mode.
        userAccountsFile = STORAGE_PATH + std::string(argv[1]);
        availableGamesFile = STORAGE_PATH + std::string(argv[2]);
        gameCollectionFile = STORAGE_PATH + std::string(argv[3]);

        // Get the current time to append to daily transaction file
        auto now = std::chrono::system_clock::now();
        auto utc = std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch()).count();

        // set daily transaction file name with current time (for this session)
        dailyTransactionFile = argc == 5 ? DAILY_TRANSACTION_FILE_LOCATION + std::string(argv[4]) 
            : (std::string)DAILY_TRANSACTION_FILE_LOCATION + "daily_transaction_" + std::to_string(utc) + ".txt";   // use generated if argument not provided
    }

    // Create an instance of SharedData to manage shared data
    SharedData sharedData;

    // Create an instance of TransactionHandler, providing SharedData and the filename for user data
    TransactionHandler handler(sharedData, userAccountsFile, availableGamesFile, gameCollectionFile, dailyTransactionFile);

    // Main program loop
    while (true)
    {
        std::string transactionCode;

        std::cout << "Enter transaction code (or 'exit' to quit): ";
        std::cin >> transactionCode;

        // Check for exit condition
        if (transactionCode == "exit")
        {
            // Generate dtf even if user exits with exit
            // if (sharedData.getCurrentUser().getUsername() != "") {
            //     handler.handleTransaction("logout");
            // }
            break; // Exit the loop and end the program
        }

        // Handle transactions using the handler
        handler.handleTransaction(transactionCode);
    }

    return 0; // End the program
}
