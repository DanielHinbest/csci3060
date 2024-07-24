import glob
from datetime import datetime, timedelta
from file_manager import FileManager

class DailyTransactionFileManager:
    """
    This class represents a file manager for daily transaction files.
    It provides methods to read and write daily transaction files.

    Attributes:
        None

    Methods:
        read: Read the daily transaction files from the previous day.
        write: Merge the daily transaction files from the previous day into a single file.

    """

    def read(self):
        """
        Read the daily transaction files from the previous day.

        Returns:
            files (list): A list of file paths for the daily transaction files from the previous day.

        """
        # Calculate yesterday's date range in UTC
        yesterday = datetime.utcnow() - timedelta(days=1)
        start_timestamp = int(yesterday.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        end_timestamp = int(yesterday.replace(hour=23, minute=59, second=59, microsecond=999999).timestamp())

        # Pattern to match all transaction files from yesterday
        files = []
        for i in range(start_timestamp, end_timestamp + 1):
            pattern = f"./storage/daily_transactions/daily_transaction_{i}.txt"
            matched_files = glob.glob(pattern)
            files.extend(matched_files)

        return files

    def write(self):
        """
        Merge the daily transaction files from the previous day into a single file.

        Returns:
            merged_filename (str): The file path of the merged transaction file.

        """
        # Find all files from yesterday
        files = self.read()
        
        # Sort files based on their creation time embedded in the filename
        files.sort(key=lambda f: int(f.split('_')[-1].split('.')[0]))

        # Create the merged file name with precise datetime
        yesterday_str = (datetime.utcnow() - timedelta(days=1)).strftime('%Y%m%d%H%M%S')
        merged_filename = f"./src/backend/storage/merged_transactions_{yesterday_str}.txt"

        # Merge the files
        # Initially create or truncate the merged file
        open(merged_filename, 'w').close()

        # Open each file and append its content to the merged file
        for filename in files:
            with open(filename, 'r') as file:
                content = file.read()
                with open(merged_filename, 'a') as merged_file:  # Open in append mode
                    merged_file.write(content)

        return merged_filename  # Indicate successful write operation
