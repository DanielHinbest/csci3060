from abc import ABC, abstractmethod
import os

class FileManager(ABC):
    """
    Abstract base class for file managers.
    """

    @abstractmethod
    def read(self, file_name):
        """
        Reads data from a file.

        Parameters:
        - file_name (str): The name of the file to read.

        Returns:
        - The data read from the file.
        """
        pass

    @abstractmethod
    def write(self, file_name, data):
        """
        Writes data to a file.

        Parameters:
        - file_name (str): The name of the file to write to.
        - data: The data to write to the file.
        """
        pass