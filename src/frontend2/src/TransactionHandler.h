#ifndef TRANSACTION_HANDLER_H
#define TRANSACTION_HANDLER_H

#include <iostream>
#include <string>
#include "AuthManager.h"
#include "UserManager.h"
#include "GameManager.h"
#include "SharedData.h"
#include "DailyTransactionWriter.h"

class TransactionHandler
{
public:
    // Constructor that takes a SharedData reference and filenames for various data
    TransactionHandler(SharedData &sharedData, const std::string &usersFilename,
                       const std::string &availableGamesFilename, const std::string gamesCollectionFilename,
                       const std::string &dailyTransactionFilename)
        : sharedData(sharedData),
          userManager(sharedData, usersFilename),
          authManager(sharedData, usersFilename),
          gameManager(sharedData, usersFilename, availableGamesFilename, gamesCollectionFilename),
          dailyTransactionWriter(dailyTransactionFilename) {}

    // Function to handle different transactions based on the provided transaction code
    void handleTransaction(const std::string &transactionCode)
    {
        if (transactionCode == "login")
        {
            handleLoginTransaction();
        }
        else if (!isLoggedIn)
        {
            std::cout << "You must login first" << std::endl;
        }
        else
        {
            handleLoggedInTransaction(transactionCode);
        }
    }

private:
    // Variable to track whether a user is logged in
    bool isLoggedIn = false;

    // Reference to the shared data object
    SharedData &sharedData;

    // AuthManager, UserManager, and GameManager instances for handling transactions
    AuthManager authManager;
    UserManager userManager;
    GameManager gameManager;

    // DailyTransactionWriter instance for recording daily transactions
    DailyTransactionWriter dailyTransactionWriter;

    // Helper function to handle the "login" transaction
    void handleLoginTransaction()
    {
        if (isLoggedIn)
        {
            std::cout << "You are already logged in" << std::endl;
        }
        else
        {
            isLoggedIn = authManager.login();
        }
    }

    // Helper function to handle transactions when the user is already logged in
    void handleLoggedInTransaction(const std::string &transactionCode)
    {
        if (transactionCode == "logout")
        {
            handleLogoutTransaction();
        }
        else if (transactionCode == "sell")
        {
            handleSellTransaction();
        }
        else if (transactionCode == "buy")
        {
            handleBuyTransaction();
        }
        else if (transactionCode == "create")
        {
            handleCreateTransaction();
        }
        else if (transactionCode == "delete")
        {
            handleDeleteTransaction();
        }
        else if (transactionCode == "refund")
        {
            handleRefundTransaction();
        }
        else if (transactionCode == "addcredit")
        {
            handleAddCreditTransaction();
        }
        else if (transactionCode == "list")
        {
            handleListTransaction();
        }
        else if (transactionCode == "listusers")
        {
            handleListUsersTransaction();
        }
        else if (transactionCode == "search") {
            handleSearchTransaction();
        }
        else
        {
            std::cout << "Invalid transaction code. Please try again." << std::endl;
        }
    }

    // Helper function to handle the "logout" transaction
    void handleLogoutTransaction()
    {
        dailyTransactionWriter.writeDailyTransactionFile(sharedData.getCurrentUser());
        isLoggedIn = !authManager.logout();

        // Now, exit the application
        // if (!isLoggedIn)
        // {
        //     std::cout << "Exiting application..." << std::endl;
        //     exit(0);
        // }
    }

    // Helper function to handle the "sell" transaction
    void handleSellTransaction()
    {
        if (sharedData.getCurrentUser().getType() == BuyStandard || sharedData.getCurrentUser().getType() == AccountsManager)
        {
            std::cout << "You do not have the privilege to sell a game." << std::endl;
        }
        else
        {
            Game game = gameManager.sellGame();

            if (game.getGameName() == "")
                return;

            dailyTransactionWriter.addSellTransaction(game);
        }
    }

    // Helper function to handle the "buy" transaction
    void handleBuyTransaction()
    {
        if (sharedData.getCurrentUser().getType() == SellStandard || sharedData.getCurrentUser().getType() == AccountsManager)
        {
            std::cout << "You do not have the privilege to sell a game." << std::endl;
        }
        else
        {
            Game game = gameManager.buyGame();

            // If buy game failed
            if (game.getGameName() == "")
                return;

            std::string buyerUsername = sharedData.getCurrentUser().getUsername();
            dailyTransactionWriter.addBuyTransaction(game, buyerUsername);
        }
    }

    // Helper function to handle the "create" transaction
    void handleCreateTransaction()
    {
        if (sharedData.getCurrentUser().getType() != Admin && sharedData.getCurrentUser().getType() != AccountsManager)
        {
            std::cout << "User unauthorized" << std::endl;
        }
        else
        {
            User user = userManager.createUser();

            // If user creation failed (e.g. AccountsManager tried to create Admin user)
            if (user.getUsername() == "")
                return;
            dailyTransactionWriter.addUserTransaction("01", user);
        }
    }

    // Helper function to handle the "delete" transaction
    void handleDeleteTransaction()
    {
        if (sharedData.getCurrentUser().getType() != Admin && sharedData.getCurrentUser().getType() != AccountsManager)
        {
            std::cout << "User unauthorized" << std::endl;
        }
        else
        {
            User deletedUser = userManager.deleteUser();

            // If user deletion failed
            if (deletedUser.getUsername() == "")
                return;

            std::string deleteUsername = deletedUser.getUsername();
            gameManager.removeUserGames(deleteUsername);
            dailyTransactionWriter.addUserTransaction("02", deletedUser);
        }
    }

    // Helper function to handle the "refund" transaction
    void handleRefundTransaction()
    {
        if (sharedData.getCurrentUser().getType() != Admin && sharedData.getCurrentUser().getType() != AccountsManager)
        {
            std::cout << "User unauthorized" << std::endl;
        }
        else
        {
            refundResult refund = userManager.refund();

            // If refund failed
            if (refund.buyerUsername == "")
                return;

            dailyTransactionWriter.addRefundTransaction(refund.buyerUsername, refund.sellerUsername, refund.creditAmount);
        }
    }

    // Helper function to handle the "addcredit" transaction
    void handleAddCreditTransaction()
    {
        if (sharedData.getCurrentUser().getType() != Admin && sharedData.getCurrentUser().getType() != AccountsManager)
        {
            std::cout << "User unauthorized" << std::endl;
        }
        else
        {
            User *user = userManager.addCredit();
            if (user != nullptr)
            {
                dailyTransactionWriter.addUserTransaction("06", *user);
            }
        }
    }

    // Helper function to handle the "list" transaction
    void handleListTransaction()
    {
        gameManager.listAvailableGames();
    }

    // Helper function to handle the "listusers" transaction
    void handleListUsersTransaction()
    {
        if (sharedData.getCurrentUser().getType() != Admin && sharedData.getCurrentUser().getType() != AccountsManager)
        {
            std::cout << "User unauthorized" << std::endl;
        }
        else
        {
            userManager.listUsers();
        }
    }

    // Helper function to handle the "search" transaction
    void handleSearchTransaction() 
    {
        std::string searchString;
        std::cout << "Enter search string: ";
        std::cin >> searchString;

        std::vector<User> users = userManager.searchUsers(searchString);
        std::vector<Game> games = gameManager.searchGames(searchString);

        if (sharedData.getCurrentUser().getType() != Admin && sharedData.getCurrentUser().getType() != AccountsManager)
        {
            users.erase(std::remove_if(users.begin(), users.end(), [](User user) {
                return user.getType() == Admin && !user.isSellingGames();
            }), users.end());
        }

        if (users.empty() && games.empty()) {
            std::cout << "No results found." << std::endl;
        } else {
            for (User user : users) {
                std::cout << user.getUsername() << std::endl;
            }

            for (Game game : games) {
                std::cout << game.getGameName() << std::endl;
            }
        }
    }
};

#endif
