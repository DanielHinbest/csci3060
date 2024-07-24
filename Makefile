MAIN_FILE_PATH = ./src/frontend2/src/main.cpp

# Rule to compile all source files
build: $(OBJECT_FILES)
	g++ $(MAIN_FILE_PATH) -o distribution-system.exe

start: 
	./distribution-system.exe currentaccounts.txt availablegames.txt gamescollection.txt

# Rule to run tests then compare the results.
run_tests:
	$(MAKE) build
	chmod +x ./scripts/run_tests.sh
	chmod +x ./scripts/check_tests.sh
	chmod +x ./scripts/output_test.sh
	chmod +x ./scripts/transaction_file_test.sh
	chmod +x ./distribution-system.exe
	bash ./scripts/run_tests.sh
	bash ./scripts/check_tests.sh

clean_tests:
	rm -fr ./testing/tests
	rm -f ./storage/daily_transactions/dtf_test_*

clean_transactions:
	rm -f ./storage/daily_transactions/daily_transaction_*

# Rule to clean the directory
clean:
	rm -f main.o distribution-system.exe
	$(MAKE) clean_tests
	$(MAKE) clean_transactions

# Rule to clean and then build the program.
rebuild: build

.PHONY: test

test:
	chmod +x run_tests.sh
	 bash run_tests.sh $(filter-out $@,$(MAKECMDGOALS))
%:
	@:

compare:
	chmod +x compare_results.sh
	 bash compare_results.sh $(filter-out $@,$(MAKECMDGOALS))
%:
	@:

run_backend:
	python3 ./storage/daily_transactions/create_test_dtf.py
	python3 ./src/backend/main.py

run_system: 
	$(MAKE) rebuild
	$(MAKE) run_tests all
	$(MAKE) run_backend

test_backend:
	@if ["$(filter-out $@,$(MAKECMDGOALS))" = ""]; then \
    	python3 -m pytest src/backend/test/; \
    else \
        python3 -m pytest src/backend/test/test_$(filter-out $@,$(MAKECMDGOALS)).py; \
    fi

test_system:
	$(MAKE) run_tests
	$(MAKE) test_backend

COLOR_RESET = \033[0m
COLOR_GREEN = \033[0;32m
COLOR_BLUE = \033[0;34m
COLOR_PURPLE = \033[0;35m
COLOR_YELLOW = \033[0;33m
# Create a help menu
help:
	@echo "$(COLOR_YELLOW)Makefile Help Menu$(COLOR_RESET)"
	@echo "------------------"
	@echo "$(COLOR_GREEN)build$(COLOR_RESET): Compile the $(COLOR_BLUE)frontend$(COLOR_RESET) source files and create the executable."
	@echo "$(COLOR_GREEN)start$(COLOR_RESET): Run the executable with the default files."
	@echo "$(COLOR_GREEN)clean$(COLOR_RESET): Remove all generated project files, executables and daily transaction files."
	@echo "$(COLOR_GREEN)rebuild$(COLOR_RESET): Clean the directory and then build the $(COLOR_BLUE)frontend$(COLOR_RESET) program."
	@echo "$(COLOR_GREEN)test$(COLOR_RESET): Run the $(COLOR_BLUE)frontend$(COLOR_RESET) tests specified in the run_tests.sh script."
	@echo "$(COLOR_GREEN)compare$(COLOR_RESET): Compare the results of the $(COLOR_BLUE)frontend$(COLOR_RESET) tests specified in the compare_results.sh script."
	@echo "$(COLOR_GREEN)run_tests$(COLOR_RESET): Run the $(COLOR_BLUE)frontend$(COLOR_RESET) tests and compare the results."
	@echo "$(COLOR_GREEN)clean_tests$(COLOR_RESET): Remove the test files and directories."
	@echo "$(COLOR_GREEN)clean_transactions$(COLOR_RESET): Remove generated daily_transaction files storage/daily_transactions."
	@echo "$(COLOR_GREEN)run_backend$(COLOR_RESET): Run the $(COLOR_PURPLE)backend$(COLOR_RESET) of the project only."
	@echo "$(COLOR_GREEN)run_system$(COLOR_RESET): Rebuilds the $(COLOR_BLUE)frontend$(COLOR_RESET), runs the front end tests and runs the $(COLOR_PURPLE)backend$(COLOR_RESET)."
	@echo "$(COLOR_GREEN)test_backend$(COLOR_RESET): Runs all the $(COLOR_PURPLE)backend$(COLOR_RESET) tests if no argument provided. To do specific, add name of module to test as arg."