#!/bin/bash

# Base directories for each day
days_base_dir="./storage/days/"
days=("day1" "day2" "day3" "day4" "day5")


# Define locations for the accounts, collection, and available games files
accounts_file="./storage/currentaccounts.txt"
collection_file="./storage/gamescollection.txt"
available_games_file="./storage/availablegames.txt"

# Loop through each day, running daily.sh with the day's directory
for day in "${days[@]}"; do
    echo "Processing $day..."

    # Define actual and expected output directories for the current day
    actual_output_dir="${days_base_dir}${day}/actual_output"
    expected_output_dir="${days_base_dir}${day}/expected_output"

    # Ensure the output directories exist
    mkdir -p "$actual_output_dir"
    mkdir -p "$expected_output_dir"

    # Call daily.sh with dynamically determined paths
    ./daily.sh "${days_base_dir}${day}" "$actual_output_dir" "$expected_output_dir" "$accounts_file" "$available_games_file" "$collection_file" 
done

echo "Weekly process complete."