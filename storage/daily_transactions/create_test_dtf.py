import os
import random
import shutil
from datetime import datetime, timedelta

# This script creates a copy of all .txt files in the current directory, with the filename format daily_transaction_<timestamp>.txt
# to allow testing of the DailyTransactionFileManager class in the backend. The timestamp is a random value within the range of yesterday.

# Specify the directory containing the .txt files
directory = "./storage/daily_transactions/"  # Adjust this path to your directory

# Calculate the timestamp range for yesterday
yesterday = datetime.utcnow() - timedelta(days=1)
start_timestamp = int(yesterday.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
end_timestamp = int(yesterday.replace(hour=23, minute=59, second=59, microsecond=999999).timestamp())

# Iterate over all .txt files in the directory
for filename in os.listdir(directory):
    #if filename.endswith(".txt") and not filename.startswith("daily_transaction_"):
    if filename.endswith(".txt"):
        # Generate a random timestamp for yesterday
        random_timestamp = random.randint(start_timestamp, end_timestamp)
        
        # Construct the new filename
        new_filename = f"daily_transaction_{random_timestamp}.txt"
        
        # Copy the file with the new filename
        shutil.copy(os.path.join(directory, filename), os.path.join(directory, new_filename))
        print(f"Copied {filename} to {new_filename}")
