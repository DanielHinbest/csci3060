# csci3060

Ontario Tech University Software Quality Assurance course project.

> Check [docs](docs) for project design documents, class diagrams etc. [LATEST DOC FOR PHASE 5](docs/Phase%205%20Testing%20Document.pdf)

## Dev

Below are instructions for development. Such as compiling and running the system. In order to run any of the make rules, you need to ensure `make` is installed on your system. Most linux distributions come with make pre-installed, but if not check documentation for how to get make installed. For the **backend**, python3 must be installed on your system.

> Run `make help` to see what each command does without reading the below information again. **In order to use make commands, ensure your current directory is the one with the Makefile.**

### Compiling and running the system

**System Requirements: Linux distribution running either natively or within WSL. For example, Ubuntu for WSL, Ubuntu virtual machine, or Ubuntu OS.**

#### Compiling Frontend

To compile code run `make build`. Then to run the code use `./distribution-system.exe <current_user_accounts> <available_games> <game_collection> (optional)<daily_transaction>` to run the executable. Where the first parameter is always the current user accounts file, the second is the available games, the third is the games collection and the final parameter is an optional daily transaction file. Note: The daily transaction file passed to the system on startup **must** be empty! make clean will clear out all output files from the system.
e.g. `./distribution-system.exe current_user_accounts.txt available_games.txt game_collection.txt`

To ensure code in the `main` branch of the repository always runs, run a `make clean` and `make build` **PRIOR** to every commit. You can also do `make rebuild` to do both of these actions in one command.

Note: g++ **must** be installed on the host machine for compilation and running the system.

#### Running Backend

To run the backend system, assuming the frontend has previously ran and produced output files, run `make run_backend`. Otherwise, if the frontend has NOT been ran or there are changes to be compiled and ran from the frontend, use `make run_system`.

**`make run_backend`**: Will compile all daily transaction files prodcued by the frontend in frontend storage with `create_tests_dtf.py` and assign each a new name in the format `daily*transaction*{date}.txt where the date is some time in the previous calendar day. **NOTE: This is only to be used for testing. Will not exist in production**. The system will then compile all the daily transaction files into one merged daily transaction file. Finally, it reads the old user accounts, game collection, and available games files then parses the merged daily transaction file to make any changes. While parsing the daily transaction file it will store a local map of each of the other files and validate against them for any potential changes.

**`make run_system`**: Will clean all executable files in the frontend, clear all daily transaction files in storage, and clean all test outputs. Then it will run the backend system. See the `run_backend` description for further details.

**Note: python3 must be installed on the host machine for compilation and running the system.**

### Creating classes

#### On the Frontend

When a class is created the header file will need to be added in `/include/<directory_name>/<header_file>`. And the .cpp file will be required to be added in the `/src/<base_class_name>/<class_name>.cpp`.

Once the files are added they will need to be referenced in the Makefile for compilation. The structure goes as follows:

- First, the header path will be needed. Add the path to the header file and name it `<CLASSNAME_HEADER_PATH>`.
- Next, the `HEADERS` variables will need to be updated to include the new header files. This can be done with `$(HEADER_PATH)filename.h`.
- Moving on, the source path for the cpp file will need to be created. Add a source path such as the following `<CLASSNAME_SOURCE_PATH>`.
- Finally, the `SOURCE_FILES` variable will need to be updated. This can be done with `$(SOURCE_PATH)classname.cpp`.

Use `make clean` to clear out the old files and `make build` to compile the new additions. If there is an error in compilation ensure the syntax is all properly defined.

#### On the Backend

Coming soon...

### Naming Conventions

Please adhere to the standard programming practices for naming conventions.

- Snake Case when creating functions and methods. e.g. `my_function`.
- Pascal for class names. e.g. `MyClass`.
- Camel case for variable names. e.g. `myVariable`.

### Adding a Transaction

Take the following steps to add a new type of transaction to the system:

- Add a new member to the `TransactionCode` enum in [transaction.h](include/transaction/transaction.h)
- Add a new private static function declaration inside `Transaction` class in [transaction.h](include/transaction/transaction.h)
- Add an entry to the `transactionCodeMap` for the transaction in [transaction.cpp](src/transaction/transaction.cpp)
- Add an entry to the `transactionFunctions` map for the transaction in [transaction.cpp](src/transaction/transaction.cpp)
- Implement the function in [transaction.cpp](src/transaction/transaction.cpp)

## Testing

### Frontend Testing

**NOTE**: Make sure to do a `make build` before your first time running the test scripts and a `make rebuild` anytime a change is made to the code.

Testing is done using the shell scripts [run_tests.sh](run_tests.sh) and [compare_results.sh](compare_results.sh). The `run_tests` script generates the folders and files in `testing/tests` and the `compare_results` script actually compares the expected results to the actual ones.

Though the script files can be used directly, it is recommended to use the rules that are implemented in the makefile as follows:

`make test <transaction>`: Tests all cases for a single transaction. `all` can be used to do all test cases at once. `make compare <transaction>`: After running `make test`, use this with the same argument to check the results of the test.

**RECOMMENDED**: You can do both of these at once by doing `make run_tests <transaction>` to generate the test files and do the comparison.

Use `make clean_tests` to remove all test-generated files, including daily transaction files, if the directory becomes bigger than you want it to.

### Backend Testing

No other component of the project needs to be compiled or ran to test the backend, just make sure python3 and [pytest](https://docs.pytest.org/en/8.0.x/) are installed on your system.

#### Recommended Method

To run the backend tests, use `make test_backend`. Running this command runs all the tests on the backend. If you wish to test only one module and not the entire suite, you can also do `make test_backend [module_name]` where `module_name` is the name of the module you want to test (e.g. `make test_backend available_games` runs the tests for available_games only)

#### Alternate

You can also just run `pytest` if it is on your PATH, and if it is not do `python3 -m pytest`. **Only do this if you wish to pass flags to pytest.**

## System

Below are high level details of the system for dev and client reference.

### Creating Users

Creating users is a privileged transaction, therefore, only admins can create users. For the purpose of the dev process there is an initial admin account created with just the plain username `admin`. Please use this account to create subsequent users, admin or otherwise, to test functionality.
