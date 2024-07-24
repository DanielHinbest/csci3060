#!/bin/bash

# Define Colours
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Usage check
if [ "$#" -ne 6 ]; then
	echo -e "${YELLOW}Usage${NC}: $0 <Input Directory> <Actual Output Directory> <Expected Output Directory> <Accounts File> <Games Collection File> <Available Games File>">&2
	exit 1
fi

# Command line arguments
input_dir="$1"
actual_output_dir="$2"
expected_output_dir="$3"
accounts_file="$4"
collection_file="$5"
available_games_file="$6"

# # Reset files so test inputs will work as intended
# > "$accounts_file"
# > "$collection_file"
# > "$available_games_file"

# # Copy corresponding files from input_dir into accounts_file, collection_file, available_games_file
# cp "storage/days/days_availablegames.txt" "$available_games_file"
# cp "storage/days/days_currentaccounts.txt" "$accounts_file"
# cp "storage/days/days_gamescollection.txt" "$collection_file"

# Ensure actual output directory exists
mkdir -p "$actual_output_dir"

# Ensure input directory exists
if [ ! -d "$input_dir" ]; then
  echo -e "${RED}Error:${NC} Input Directory ${input_dir} does not exist." >&2
  exit 1
fi

# Ensure expected output directory exists
if [ ! -d "$expected_output_dir" ]; then
  echo -e "${RED}Error:${NC} Expected output directory ${expected_output_dir} does not exist." >&2
  exit 1
fi

# Ensure accounts file exists
if [ ! -f "$accounts_file" ]; then
  echo -e "${RED}Error:${NC} Accounts file ${accounts_file} does not exist." >&2
  exit 1
fi

# Ensure collection file exists
if [ ! -f "$collection_file" ]; then
  echo -e"${RED}Error:${NC} Collection file ${collection_file} does not exist." >&2
  exit 1
fi

# Ensure available games file exists
if [ ! -f "$available_games_file" ]; then
  echo -e "${RED}Error:${NC} Available games file ${available_games_file} does not exist." >&2
  exit 1
fi

# Loop through all .in files in the input directory
for in_file in "$input_dir"/*.inp; do
  # Increment counter
  counter=$((counter + 1))
  # Extract filename without extension
  base_name=$(basename "$in_file" .inp)
  # Define output filename for .out files
  out_file="$actual_output_dir/$base_name.out"
  daily_transaction_file="$input_dir/daily_transaction_$counter.txt"
  # Empty daily_transaction file (if it already exists)
  > "$daily_transaction_file"
  # Run the C++ program with the necessary files (last inp file needs to exit to go next loop)
  cat "$in_file" | ./distribution-system.exe "$accounts_file" "$collection_file" "$available_games_file" "$daily_transaction_file" > "$out_file"
done


# Merge all daily transaction files into merged_daily
cat "$input_dir"/daily_transaction*.txt > "$input_dir"/merged_daily.txt

# Run backend.py on the merged file
python3 ./src/backend/main.py "$input_dir"/merged_daily.txt

# Define the log file path
diff_log_file="daily_diff_log.txt"

# Ensure the log file is empty at the start
> "$diff_log_file"

# Loop through all .out files in the actual output directory for comparison
for out_file in "$actual_output_dir"/*.out; do
  # Extract filename for comparison
  base_name=$(basename "$out_file")
  # Compare .out files and append to log
  echo "Comparing $base_name with expected output..." >> "$diff_log_file"
  diff "$out_file" "$expected_output_dir/$base_name" >> "$diff_log_file" 2>&1
done

# Compare the Merged file and append to log
echo "Comparing Merged daily transaction file with expected output..." >> "$diff_log_file"
diff "$input_dir"/merged_daily.txt "$expected_output_dir/merged_daily.txt" >> "$diff_log_file" 2>&1

# Compare the three base files against their expected counterparts and append to log
echo "Comparing base files with expected outputs..." >> "$diff_log_file"
diff "$accounts_file" "$expected_output_dir/$(basename "$accounts_file")" >> "$diff_log_file" 2>&1
diff "$collection_file" "$expected_output_dir/$(basename "$collection_file")" >> "$diff_log_file" 2>&1
diff "$available_games_file" "$expected_output_dir/$(basename "$available_games_file")" >> "$diff_log_file" 2>&1
