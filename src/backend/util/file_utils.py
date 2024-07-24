# Houses all utility functions to help with file functionality
import os

def change_to_file_dir(file):
    """
    Changes to the directory in the filepath
    """
    abspath = os.path.abspath(file)
    dname = os.path.dirname(abspath)
    os.chdir(dname)